const state = {
  token: null,
  user: null,
  recordsPayload: null,
  ehealthCardPayload: null,
};

function renderOutput(targetId, payload) {
  const target = document.getElementById(targetId);
  if (!target) {
    return;
  }
  target.textContent = JSON.stringify(payload, null, 2);
}

function buildFallbackCardPhoto(name, healthId) {
  const primary = String(name || healthId || "P").trim().toUpperCase();
  const initials = primary.slice(0, 2) || "P";
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="280" height="280">
      <rect width="100%" height="100%" fill="#d6e3dd"/>
      <text x="50%" y="56%" dominant-baseline="middle" text-anchor="middle"
        font-family="Arial, sans-serif" font-size="86" fill="#2a5d57">${initials}</text>
    </svg>
  `;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}

function renderEHealthCard(card) {
  const nameNode = document.getElementById("ehealth-name");
  const idNode = document.getElementById("ehealth-id");
  const bloodNode = document.getElementById("ehealth-blood-group");
  const phoneNode = document.getElementById("ehealth-phone");
  const photoNode = document.getElementById("ehealth-photo");

  if (nameNode) {
    nameNode.textContent = card.name || "-";
  }
  if (idNode) {
    idNode.textContent = card.health_id || "-";
  }
  if (bloodNode) {
    bloodNode.textContent = card.blood_group || "-";
  }
  if (phoneNode) {
    phoneNode.textContent = card.phone || "-";
  }
  if (photoNode) {
    const fallback = buildFallbackCardPhoto(card.name, card.health_id);
    photoNode.src = card.photo_url || fallback;
    photoNode.onerror = () => {
      photoNode.src = fallback;
    };
  }
}

function extractDownloadName(response, fallbackName) {
  const disposition = response.headers.get("content-disposition") || "";
  const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
  if (utf8Match && utf8Match[1]) {
    return decodeURIComponent(utf8Match[1]);
  }

  const plainMatch = disposition.match(/filename="?([^";]+)"?/i);
  if (plainMatch && plainMatch[1]) {
    return plainMatch[1];
  }

  return fallbackName;
}

async function downloadRecordFile(downloadUrl, fallbackName) {
  const response = await fetch(downloadUrl, {
    headers: {
      Authorization: `Bearer ${state.token}`,
    },
  });

  if (!response.ok) {
    let message = `Download failed with status ${response.status}`;
    try {
      const json = await response.json();
      message = HC.parseApiError(json, message);
    } catch {
      // Keep default message.
    }
    throw new Error(message);
  }

  const blob = await response.blob();
  const fileName = extractDownloadName(response, fallbackName);
  const fileUrl = URL.createObjectURL(blob);

  const anchor = document.createElement("a");
  anchor.href = fileUrl;
  anchor.download = fileName;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();

  URL.revokeObjectURL(fileUrl);
}

function renderRecordsList(payload) {
  const container = document.getElementById("records-container");
  if (!container) {
    return;
  }

  container.innerHTML = "";
  const records = Array.isArray(payload.records) ? payload.records : [];

  if (records.length === 0) {
    const empty = document.createElement("p");
    empty.className = "hint";
    empty.textContent = "No records available.";
    container.appendChild(empty);
    return;
  }

  records.forEach((record) => {
    const card = document.createElement("article");
    card.className = "card record-card";

    const title = document.createElement("h3");
    title.textContent = `${record.record_type || "Record"} (${record.timestamp || ""})`;

    const info = document.createElement("p");
    info.className = "hint";
    info.textContent = record.description || "No description";

    const hash = document.createElement("p");
    hash.className = "hint";
    hash.textContent = `Hash: ${record.record_hash || "n/a"}`;

    const originalButton = document.createElement("button");
    originalButton.type = "button";
    originalButton.textContent = "Download File";
    originalButton.disabled = !record.download_url;
    originalButton.addEventListener("click", async () => {
      try {
        await downloadRecordFile(record.download_url, record.file_name || "record-file");
        HC.showStatus("File downloaded.", "good");
      } catch (error) {
        HC.showStatus(error.message, "bad", 5000);
      }
    });

    const summaryButton = document.createElement("button");
    summaryButton.type = "button";
    summaryButton.textContent = "Download Summary";
    summaryButton.disabled = !record.summary_download_url;
    summaryButton.addEventListener("click", async () => {
      try {
        await downloadRecordFile(
          record.summary_download_url,
          record.summary_file_name || "record-summary.txt",
        );
        HC.showStatus("Summary downloaded.", "good");
      } catch (error) {
        HC.showStatus(error.message, "bad", 5000);
      }
    });

    const actions = document.createElement("div");
    actions.className = "record-actions";
    actions.appendChild(originalButton);
    actions.appendChild(summaryButton);

    card.appendChild(title);
    card.appendChild(info);
    card.appendChild(hash);
    card.appendChild(actions);
    container.appendChild(card);
  });
}

function wireLogout() {
  document.getElementById("logout-btn")?.addEventListener("click", async () => {
    await HC.logout(state.token);
    window.location.href = "/app";
  });
}

function wireLoadRecords() {
  document.getElementById("load-records-btn")?.addEventListener("click", async () => {
    try {
      const response = await HC.apiRequest("/patient/me", {
        token: state.token,
      });
      state.recordsPayload = response;
      renderOutput("records-output", response);
      renderRecordsList(response);
      HC.showStatus("Records loaded.", "good");
    } catch (error) {
      renderOutput("records-output", { error: error.message });
      HC.showStatus(error.message, "bad");
    }
  });
}

async function loadEHealthCard() {
  const response = await HC.apiRequest("/patient/me/e-healthcard", {
    token: state.token,
  });
  state.ehealthCardPayload = response;
  renderEHealthCard(response);
  return response;
}

function wireLoadEHealthCard() {
  document.getElementById("load-ehealth-card-btn")?.addEventListener("click", async () => {
    try {
      await loadEHealthCard();
      HC.showStatus("E-healthcard loaded.", "good");
    } catch (error) {
      HC.showStatus(error.message, "bad", 5000);
    }
  });
}

async function boot() {
  const restored = await HC.restoreSessionFromStorage();
  if (!restored) {
    window.location.href = "/app";
    return;
  }

  state.token = restored.token;
  state.user = restored.session.user;

  if (state.user.role !== "patient") {
    HC.redirectToRole(state.user.role);
    return;
  }

  if (!state.user.health_id) {
    HC.showStatus("Your account is missing HealthID assignment. Contact admin.", "bad", 7000);
    return;
  }

  HC.setUserBadge(state.user);
  const healthLabel = document.getElementById("health-id-label");
  if (healthLabel) {
    healthLabel.textContent = state.user.health_id;
  }

  wireLogout();
  wireLoadEHealthCard();
  wireLoadRecords();
  try {
    await loadEHealthCard();
  } catch (error) {
    HC.showStatus(error.message, "bad", 5000);
  }
}

boot().catch((error) => {
  HC.showStatus(error.message || "Unable to initialize patient workspace.", "bad", 7000);
});
