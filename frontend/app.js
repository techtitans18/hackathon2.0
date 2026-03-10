const AUTH_TOKEN_KEY = "healthcare_blockchain_auth_token";

const state = {
  token: null,
  user: null,
  statusTimer: null,
};

function byId(id) {
  return document.getElementById(id);
}

function showStatus(message, type = "good", durationMs = 3800) {
  const banner = byId("status-banner");
  if (!banner) {
    return;
  }
  banner.textContent = message;
  banner.className = `status status-${type}`;

  if (state.statusTimer) {
    clearTimeout(state.statusTimer);
  }
  state.statusTimer = setTimeout(() => {
    banner.className = "status hidden";
  }, durationMs);
}

function formatOutput(payload) {
  return JSON.stringify(payload, null, 2);
}

function renderOutput(targetId, payload) {
  const target = byId(targetId);
  if (!target) {
    return;
  }
  target.textContent = formatOutput(payload);
}

function setAuthState(isAuthenticated) {
  byId("auth-panel")?.classList.toggle("hidden", isAuthenticated);
  byId("app-shell")?.classList.toggle("hidden", !isAuthenticated);
}

function setUserBadge(user) {
  byId("user-name").textContent = user.name || "Signed in user";
  byId("user-email").textContent = user.email || "";
  const picture = byId("user-picture");
  if (picture) {
    picture.src = user.picture || "";
    picture.style.visibility = user.picture ? "visible" : "hidden";
  }
}

function clearUserBadge() {
  byId("user-name").textContent = "";
  byId("user-email").textContent = "";
  const picture = byId("user-picture");
  if (picture) {
    picture.src = "";
    picture.style.visibility = "hidden";
  }
}

function parseApiError(raw, fallback) {
  if (raw && typeof raw === "object") {
    if (typeof raw.detail === "string") {
      return raw.detail;
    }
    if (Array.isArray(raw.detail)) {
      return raw.detail.map((entry) => entry.msg || "Validation error").join(", ");
    }
  }
  return fallback;
}

async function apiRequest(path, options = {}) {
  const {
    method = "GET",
    jsonBody = null,
    formBody = null,
    requireAuth = true,
  } = options;
  const headers = {};

  if (requireAuth) {
    if (!state.token) {
      throw new Error("Please sign in first.");
    }
    headers.Authorization = `Bearer ${state.token}`;
  }

  if (jsonBody !== null) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(path, {
    method,
    headers,
    body: jsonBody !== null ? JSON.stringify(jsonBody) : formBody,
  });

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    throw new Error(
      parseApiError(payload, `Request failed with status ${response.status}`),
    );
  }
  return payload;
}

async function waitForGoogleSdk(timeoutMs = 10000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    if (window.google && google.accounts && google.accounts.id) {
      return;
    }
    await new Promise((resolve) => setTimeout(resolve, 120));
  }
  throw new Error("Google script did not load.");
}

async function handleGoogleResponse(response) {
  if (!response || !response.credential) {
    showStatus("Google login failed. Missing credential.", "bad");
    return;
  }

  try {
    const authResponse = await apiRequest("/auth/google", {
      method: "POST",
      jsonBody: { credential: response.credential },
      requireAuth: false,
    });

    state.token = authResponse.access_token;
    state.user = authResponse.user;
    localStorage.setItem(AUTH_TOKEN_KEY, state.token);

    setUserBadge(state.user);
    setAuthState(true);
    showStatus("Google login successful.", "good");
  } catch (error) {
    showStatus(error.message || "Unable to authenticate.", "bad", 5200);
  }
}

async function restoreSessionFromStorage() {
  const savedToken = localStorage.getItem(AUTH_TOKEN_KEY);
  if (!savedToken) {
    return false;
  }

  state.token = savedToken;
  try {
    const session = await apiRequest("/auth/session");
    state.user = session.user;
    setUserBadge(state.user);
    setAuthState(true);
    return true;
  } catch {
    state.token = null;
    state.user = null;
    localStorage.removeItem(AUTH_TOKEN_KEY);
    return false;
  }
}

async function initializeGoogleButton() {
  const hint = byId("auth-hint");
  let config = null;
  try {
    config = await apiRequest("/auth/google/config", { requireAuth: false });
  } catch {
    hint.textContent = "Unable to load Google login config from backend.";
    return;
  }

  if (!config.enabled || !config.google_client_id) {
    hint.textContent =
      "Set GOOGLE_CLIENT_ID and AUTH_SECRET_KEY in backend environment, then refresh this page.";
    return;
  }

  hint.textContent = "Use the official Google Identity sign-in.";

  try {
    await waitForGoogleSdk();
  } catch (error) {
    hint.textContent = error.message;
    return;
  }

  google.accounts.id.initialize({
    client_id: config.google_client_id,
    callback: handleGoogleResponse,
    ux_mode: "popup",
    auto_select: false,
    cancel_on_tap_outside: true,
  });

  google.accounts.id.renderButton(byId("google-signin-host"), {
    type: "standard",
    shape: "pill",
    theme: "filled_blue",
    size: "large",
    text: "signin_with",
    width: 320,
  });
}

async function handleLogout() {
  try {
    await apiRequest("/auth/logout", { method: "POST" });
  } catch {
    // Ignore backend logout errors and clear local state.
  }

  state.token = null;
  state.user = null;
  localStorage.removeItem(AUTH_TOKEN_KEY);
  clearUserBadge();
  setAuthState(false);
  showStatus("Logged out.", "good");
}

function wirePatientForm() {
  const form = byId("patient-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);

    const payload = {
      name: String(data.get("name") || "").trim(),
      age: Number(data.get("age") || 0),
      phone: String(data.get("phone") || "").trim(),
    };

    try {
      const response = await apiRequest("/register_patient", {
        method: "POST",
        jsonBody: payload,
      });
      renderOutput("patient-form-output", response);

      const healthId = response.HealthID || "";
      byId("record-form").elements.HealthID.value = healthId;
      byId("lookup-patient-form").elements.HealthID.value = healthId;
      showStatus("Patient registered.", "good");
      form.reset();
    } catch (error) {
      renderOutput("patient-form-output", { error: error.message });
      showStatus(error.message, "bad");
    }
  });
}

function wireHospitalForm() {
  const form = byId("hospital-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);

    const payload = {
      hospital_name: String(data.get("hospital_name") || "").trim(),
      hospital_type: String(data.get("hospital_type") || "").trim(),
    };

    try {
      const response = await apiRequest("/register_hospital", {
        method: "POST",
        jsonBody: payload,
      });
      renderOutput("hospital-form-output", response);

      const hospitalId = response.HospitalID || "";
      byId("record-form").elements.HospitalID.value = hospitalId;
      showStatus("Hospital registered.", "good");
      form.reset();
    } catch (error) {
      renderOutput("hospital-form-output", { error: error.message });
      showStatus(error.message, "bad");
    }
  });
}

function wireRecordForm() {
  const form = byId("record-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = new FormData(form);
    const file = data.get("file");
    if (!(file instanceof File) || file.size === 0) {
      showStatus("Please choose a non-empty file.", "bad");
      return;
    }

    try {
      const response = await apiRequest("/add_record", {
        method: "POST",
        formBody: data,
      });
      renderOutput("record-form-output", response);

      if (response.record_hash) {
        byId("lookup-hash-form").elements.record_hash.value = response.record_hash;
      }
      showStatus("Record added and block created.", "good");
      form.reset();
    } catch (error) {
      renderOutput("record-form-output", { error: error.message });
      showStatus(error.message, "bad");
    }
  });
}

function wirePatientLookupForm() {
  const form = byId("lookup-patient-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const healthId = String(data.get("HealthID") || "").trim();
    if (!healthId) {
      showStatus("HealthID is required.", "bad");
      return;
    }

    try {
      const response = await apiRequest(`/patient/${encodeURIComponent(healthId)}`);
      renderOutput("lookup-patient-output", response);
      showStatus("Patient record loaded.", "good");
    } catch (error) {
      renderOutput("lookup-patient-output", { error: error.message });
      showStatus(error.message, "bad");
    }
  });
}

function wireHashLookupForm() {
  const form = byId("lookup-hash-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const hash = String(data.get("record_hash") || "").trim().toLowerCase();
    if (!/^[a-f0-9]{64}$/.test(hash)) {
      showStatus("Record hash must be 64 hex characters.", "bad");
      return;
    }

    try {
      const response = await apiRequest(`/record/hash/${hash}`);
      renderOutput("lookup-hash-output", response);
      showStatus("Hash lookup complete.", "good");
    } catch (error) {
      renderOutput("lookup-hash-output", { error: error.message });
      showStatus(error.message, "bad");
    }
  });
}

function wireBlockchainButton() {
  byId("blockchain-btn").addEventListener("click", async () => {
    try {
      const response = await apiRequest("/blockchain");
      renderOutput("blockchain-output", response);
      showStatus("Blockchain loaded.", "good");
    } catch (error) {
      renderOutput("blockchain-output", { error: error.message });
      showStatus(error.message, "bad");
    }
  });
}

async function boot() {
  setAuthState(false);
  wirePatientForm();
  wireHospitalForm();
  wireRecordForm();
  wirePatientLookupForm();
  wireHashLookupForm();
  wireBlockchainButton();
  byId("logout-btn").addEventListener("click", handleLogout);

  const restored = await restoreSessionFromStorage();
  if (restored) {
    showStatus("Session restored.", "good", 2000);
  }
  await initializeGoogleButton();
}

boot().catch((error) => {
  showStatus(error.message || "Unable to initialize frontend.", "bad", 7000);
});
