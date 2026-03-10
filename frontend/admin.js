const state = {
  token: null,
  user: null,
};

function renderOutput(targetId, payload) {
  const target = document.getElementById(targetId);
  if (!target) {
    return;
  }
  target.textContent = JSON.stringify(payload, null, 2);
}

function updateRoleFieldVisibility(role) {
  const healthRow = document.getElementById("health-id-row");
  const hospitalRow = document.getElementById("hospital-id-row");
  const healthInput = healthRow?.querySelector("input");
  const hospitalInput = hospitalRow?.querySelector("input");

  if (role === "patient") {
    healthRow?.classList.remove("hidden");
    hospitalRow?.classList.add("hidden");
    if (healthInput) {
      healthInput.required = true;
    }
    if (hospitalInput) {
      hospitalInput.required = false;
      hospitalInput.value = "";
    }
    return;
  }

  if (role === "hospital") {
    healthRow?.classList.add("hidden");
    hospitalRow?.classList.remove("hidden");
    if (healthInput) {
      healthInput.required = false;
      healthInput.value = "";
    }
    if (hospitalInput) {
      hospitalInput.required = true;
    }
    return;
  }

  healthRow?.classList.add("hidden");
  hospitalRow?.classList.add("hidden");
  if (healthInput) {
    healthInput.required = false;
    healthInput.value = "";
  }
  if (hospitalInput) {
    hospitalInput.required = false;
    hospitalInput.value = "";
  }
}

function wireLogout() {
  document.getElementById("logout-btn")?.addEventListener("click", async () => {
    await HC.logout(state.token);
    window.location.href = "/app";
  });
}

function wireHospitalForm() {
  const form = document.getElementById("hospital-form");
  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);

    const payload = {
      hospital_name: String(data.get("hospital_name") || "").trim(),
      hospital_type: String(data.get("hospital_type") || "").trim(),
    };

    try {
      const response = await HC.apiRequest("/register_hospital", {
        method: "POST",
        token: state.token,
        jsonBody: payload,
      });
      renderOutput("hospital-output", response);
      HC.showStatus("Hospital registered.", "good");
      form.reset();
    } catch (error) {
      renderOutput("hospital-output", { error: error.message });
      HC.showStatus(error.message, "bad");
    }
  });
}

function wireUserForm() {
  const form = document.getElementById("user-form");
  const roleSelect = document.getElementById("role-select");

  roleSelect?.addEventListener("change", () => {
    updateRoleFieldVisibility(roleSelect.value);
  });
  updateRoleFieldVisibility(roleSelect?.value || "hospital");

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);

    const payload = {
      email: String(data.get("email") || "").trim().toLowerCase(),
      role: String(data.get("role") || "").trim(),
      name: String(data.get("name") || "").trim() || null,
      health_id: String(data.get("health_id") || "").trim() || null,
      hospital_id: String(data.get("hospital_id") || "").trim() || null,
      is_active: String(data.get("is_active") || "true") === "true",
    };

    try {
      const response = await HC.apiRequest("/admin/users", {
        method: "POST",
        token: state.token,
        jsonBody: payload,
      });
      renderOutput("user-output", response);
      HC.showStatus("User access saved.", "good");
    } catch (error) {
      renderOutput("user-output", { error: error.message });
      HC.showStatus(error.message, "bad", 5000);
    }
  });
}

function wireUsersListButton() {
  const button = document.getElementById("load-users-btn");
  button?.addEventListener("click", async () => {
    try {
      const response = await HC.apiRequest("/admin/users", {
        token: state.token,
      });
      renderOutput("users-list-output", response);
      HC.showStatus("Users loaded.", "good");
    } catch (error) {
      renderOutput("users-list-output", { error: error.message });
      HC.showStatus(error.message, "bad");
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

  if (state.user.role !== "admin") {
    HC.redirectToRole(state.user.role);
    return;
  }

  HC.setUserBadge(state.user);
  wireLogout();
  wireHospitalForm();
  wireUserForm();
  wireUsersListButton();
}

boot().catch((error) => {
  HC.showStatus(error.message || "Unable to initialize admin workspace.", "bad", 7000);
});
