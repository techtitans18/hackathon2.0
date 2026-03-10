const state = {
  token: null,
  user: null,
};

const DASHBOARD_PANELS = {
  welcome: "hospital-panel-welcome",
  patient: "hospital-panel-patient",
  emergency: "hospital-panel-emergency",
};

function renderOutput(targetId, payload) {
  const target = document.getElementById(targetId);
  if (!target) {
    return;
  }
  target.textContent = JSON.stringify(payload, null, 2);
}

function showDashboardPanel(panelKey) {
  const activeKey = Object.prototype.hasOwnProperty.call(DASHBOARD_PANELS, panelKey)
    ? panelKey
    : "welcome";

  Object.entries(DASHBOARD_PANELS).forEach(([key, elementId]) => {
    const panel = document.getElementById(elementId);
    if (panel) {
      panel.classList.toggle("hidden", key !== activeKey);
    }
  });

  document.querySelectorAll(".dashboard-tab").forEach((button) => {
    const isActive = button.dataset.panel === activeKey;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-current", isActive ? "page" : "false");
  });
}

function wireDashboardNavigation() {
  document.querySelectorAll(".dashboard-tab").forEach((button) => {
    button.addEventListener("click", () => {
      showDashboardPanel(String(button.dataset.panel || "welcome"));
    });
  });

  document.getElementById("go-patient-module")?.addEventListener("click", () => {
    showDashboardPanel("patient");
  });

  document.getElementById("go-emergency-module")?.addEventListener("click", () => {
    showDashboardPanel("emergency");
  });
}

function wireLogout() {
  document.getElementById("logout-btn")?.addEventListener("click", async () => {
    await HC.logout(state.token);
    window.location.href = "/app";
  });
}

function wirePatientForm() {
  const form = document.getElementById("patient-form");
  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);

    const payload = {
      name: String(data.get("name") || "").trim(),
      age: Number(data.get("age") || 0),
      phone: String(data.get("phone") || "").trim(),
      dob: String(data.get("dob") || "").trim(),
      blood_group: String(data.get("blood_group") || "").trim(),
      email: String(data.get("email") || "").trim().toLowerCase(),
      photo_url: String(data.get("photo_url") || "").trim() || null,
    };

    try {
      const response = await HC.apiRequest("/register_patient", {
        method: "POST",
        token: state.token,
        jsonBody: payload,
      });
      renderOutput("patient-output", response);

      const healthId = String(response.HealthID || "").trim();
      const recordHealthIdInput = document.getElementById("record-health-id");
      if (recordHealthIdInput) {
        recordHealthIdInput.value = healthId;
      }
      const emergencyHealthIdInput = document.getElementById("emergency-profile-health-id");
      if (emergencyHealthIdInput) {
        emergencyHealthIdInput.value = healthId;
      }
      const emergencyUpsertHealthId = document.getElementById("emergency-upsert-health-id");
      if (emergencyUpsertHealthId) {
        emergencyUpsertHealthId.value = healthId;
      }
      const emergencyUpsertBloodGroup = document.getElementById("emergency-upsert-blood-group");
      if (emergencyUpsertBloodGroup) {
        emergencyUpsertBloodGroup.value = payload.blood_group;
      }
      const emergencyUpsertContact = document.getElementById("emergency-upsert-contact");
      if (emergencyUpsertContact) {
        emergencyUpsertContact.value = payload.phone;
      }

      HC.showStatus("Patient details added successfully.", "good");
      form.reset();
    } catch (error) {
      renderOutput("patient-output", { error: error.message });
      HC.showStatus(error.message, "bad");
    }
  });
}

function parseCsvList(rawValue) {
  const value = String(rawValue || "").trim();
  if (!value) {
    return [];
  }
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function wireRecordForm() {
  const form = document.getElementById("record-form");
  form?.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = new FormData(form);
    const file = data.get("file");
    if (!(file instanceof File) || file.size === 0) {
      HC.showStatus("Please choose a non-empty file.", "bad");
      return;
    }

    const hospitalId = state.user?.hospital_id || "";
    data.set("HospitalID", hospitalId);

    try {
      const response = await HC.apiRequest("/add_record", {
        method: "POST",
        token: state.token,
        formBody: data,
      });
      renderOutput("record-output", response);
      HC.showStatus("Medical report added successfully.", "good");

      const keptHealthId = String(data.get("HealthID") || "").trim();
      form.reset();
      form.elements.HospitalID.value = hospitalId;
      form.elements.HealthID.value = keptHealthId;
    } catch (error) {
      renderOutput("record-output", { error: error.message });
      HC.showStatus(error.message, "bad", 5000);
    }
  });
}

function wireEmergencyForms() {
  const upsertForm = document.getElementById("emergency-upsert-form");
  const searchForm = document.getElementById("emergency-search-form");
  const profileForm = document.getElementById("emergency-profile-form");
  const searchTypeInput = document.getElementById("emergency-search-type");
  const valueField = document.getElementById("emergency-value-field");
  const valueInput = document.getElementById("emergency-value-input");
  const nameField = document.getElementById("emergency-name-field");
  const nameInput = document.getElementById("emergency-name-input");
  const dobField = document.getElementById("emergency-dob-field");
  const dobInput = document.getElementById("emergency-dob-input");
  const emergencyProfileHealthId = document.getElementById("emergency-profile-health-id");

  const applySearchType = () => {
    const searchType = String(searchTypeInput?.value || "").trim();
    const isNameDobMode = searchType === "name_dob";

    valueField?.classList.toggle("hidden", isNameDobMode);
    nameField?.classList.toggle("hidden", !isNameDobMode);
    dobField?.classList.toggle("hidden", !isNameDobMode);

    if (valueInput) {
      valueInput.required = !isNameDobMode;
      valueInput.placeholder = searchType === "phone" ? "Enter Phone Number" : "Enter HealthID";
    }
    if (nameInput) {
      nameInput.required = isNameDobMode;
    }
    if (dobInput) {
      dobInput.required = isNameDobMode;
    }
  };

  searchTypeInput?.addEventListener("change", applySearchType);
  applySearchType();

  upsertForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(upsertForm);
    const payload = {
      role: String(state.user?.role || "hospital"),
      health_id: String(data.get("health_id") || "").trim(),
      blood_group: String(data.get("blood_group") || "").trim(),
      emergency_contact: String(data.get("emergency_contact") || "").trim(),
      allergies: parseCsvList(data.get("allergies")),
      diseases: parseCsvList(data.get("diseases")),
      surgeries: parseCsvList(data.get("surgeries")),
    };

    try {
      const response = await HC.apiRequest("/emergency/upsert", {
        method: "POST",
        token: state.token,
        jsonBody: payload,
      });
      renderOutput("emergency-upsert-output", response);

      const emergencyProfileHealthId = document.getElementById("emergency-profile-health-id");
      if (emergencyProfileHealthId) {
        emergencyProfileHealthId.value = payload.health_id;
      }
      const recordHealthIdInput = document.getElementById("record-health-id");
      if (recordHealthIdInput) {
        recordHealthIdInput.value = payload.health_id;
      }
      HC.showStatus("Emergency data saved.", "good");
    } catch (error) {
      renderOutput("emergency-upsert-output", { error: error.message });
      HC.showStatus(error.message, "bad", 5000);
    }
  });

  searchForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(searchForm);
    const searchType = String(data.get("search_type") || "").trim();
    const payload = {
      role: String(state.user?.role || "hospital"),
      search_type: searchType,
    };

    if (searchType === "name_dob") {
      payload.name = String(data.get("name") || "").trim();
      payload.dob = String(data.get("dob") || "").trim();
    } else {
      payload.value = String(data.get("value") || "").trim();
    }

    try {
      const response = await HC.apiRequest("/emergency/search", {
        method: "POST",
        token: state.token,
        jsonBody: payload,
      });
      renderOutput("emergency-search-output", response);

      const healthId = String(response.health_id || "").trim();
      if (emergencyProfileHealthId) {
        emergencyProfileHealthId.value = healthId;
      }
      const emergencyUpsertHealthId = document.getElementById("emergency-upsert-health-id");
      if (emergencyUpsertHealthId) {
        emergencyUpsertHealthId.value = healthId;
      }
      const recordHealthIdInput = document.getElementById("record-health-id");
      if (recordHealthIdInput) {
        recordHealthIdInput.value = healthId;
      }

      HC.showStatus("Emergency patient found.", "good");
    } catch (error) {
      renderOutput("emergency-search-output", { error: error.message });
      HC.showStatus(error.message, "bad", 5000);
    }
  });

  profileForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(profileForm);
    const payload = {
      role: String(state.user?.role || "hospital"),
      health_id: String(data.get("health_id") || "").trim(),
    };

    try {
      const response = await HC.apiRequest("/emergency/profile", {
        method: "POST",
        token: state.token,
        jsonBody: payload,
      });
      renderOutput("emergency-profile-output", response);

      if (response.blockchain_status === "Verified") {
        HC.showStatus("Emergency profile verified.", "good");
      } else {
        HC.showStatus("Emergency profile loaded with tamper warning.", "bad", 6500);
      }
    } catch (error) {
      renderOutput("emergency-profile-output", { error: error.message });
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

  if (state.user.role !== "hospital") {
    HC.redirectToRole(state.user.role);
    return;
  }

  if (!state.user.hospital_id) {
    HC.showStatus("Your account is missing hospital assignment. Contact admin.", "bad", 7000);
    return;
  }

  HC.setUserBadge(state.user);
  const hospitalField = document.getElementById("record-hospital-id");
  if (hospitalField) {
    hospitalField.value = state.user.hospital_id;
  }

  wireLogout();
  wireDashboardNavigation();
  wirePatientForm();
  wireRecordForm();
  wireEmergencyForms();
  showDashboardPanel("welcome");
}

boot().catch((error) => {
  HC.showStatus(error.message || "Unable to initialize hospital workspace.", "bad", 7000);
});
