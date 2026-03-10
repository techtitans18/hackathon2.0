const AUTH_TOKEN_KEY = "healthcare_blockchain_auth_token";

const ROLE_PATHS = {
  admin: "/app/admin",
  hospital: "/app/hospital",
  patient: "/app/patient",
};

function parseApiError(raw, fallback) {
  if (raw && typeof raw === "object") {
    if (typeof raw.error === "string") {
      return raw.error;
    }
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
    token = null,
    jsonBody = null,
    formBody = null,
    requireAuth = true,
  } = options;

  const headers = {};

  if (requireAuth) {
    if (!token) {
      throw new Error("Please sign in first.");
    }
    headers.Authorization = `Bearer ${token}`;
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

function getStoredToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY);
}

function saveToken(token) {
  localStorage.setItem(AUTH_TOKEN_KEY, token);
}

function clearToken() {
  localStorage.removeItem(AUTH_TOKEN_KEY);
}

async function restoreSessionFromStorage() {
  const token = getStoredToken();
  if (!token) {
    return null;
  }

  try {
    const session = await apiRequest("/auth/session", { token });
    return { token, session };
  } catch {
    clearToken();
    return null;
  }
}

function roleToPath(role) {
  return ROLE_PATHS[role] || "/app";
}

function redirectToRole(role) {
  const target = roleToPath(role);
  if (window.location.pathname !== target) {
    window.location.href = target;
  }
}

function showStatus(message, type = "good", durationMs = 4000, bannerId = "status-banner") {
  const banner = document.getElementById(bannerId);
  if (!banner) {
    return;
  }

  banner.textContent = message;
  banner.className = `status status-${type}`;

  window.setTimeout(() => {
    banner.className = "status hidden";
  }, durationMs);
}

function setUserBadge(user) {
  const name = document.getElementById("user-name");
  const email = document.getElementById("user-email");
  const picture = document.getElementById("user-picture");

  if (name) {
    name.textContent = user.name || "Signed in user";
  }
  if (email) {
    email.textContent = user.email || "";
  }
  if (picture) {
    picture.src = user.picture || "";
    picture.style.visibility = user.picture ? "visible" : "hidden";
  }
}

async function logout(token) {
  try {
    await apiRequest("/auth/logout", { method: "POST", token });
  } catch {
    // Ignore logout API failures; clear local state anyway.
  }
  clearToken();
}

window.HC = {
  AUTH_TOKEN_KEY,
  apiRequest,
  clearToken,
  getStoredToken,
  logout,
  parseApiError,
  redirectToRole,
  restoreSessionFromStorage,
  roleToPath,
  saveToken,
  setUserBadge,
  showStatus,
};
