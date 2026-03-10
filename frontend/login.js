const state = {
  token: null,
};

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
    HC.showStatus("Google login failed. Missing credential.", "bad");
    return;
  }

  try {
    const authResponse = await HC.apiRequest("/auth/google", {
      method: "POST",
      jsonBody: { credential: response.credential },
      requireAuth: false,
    });

    state.token = authResponse.access_token;
    HC.saveToken(state.token);

    HC.showStatus("Login successful. Redirecting...", "good", 1500);
    HC.redirectToRole(authResponse.user.role);
  } catch (error) {
    HC.showStatus(error.message || "Unable to authenticate.", "bad", 5200);
  }
}

async function initializeGoogleButton() {
  const hint = document.getElementById("auth-hint");
  let config;

  try {
    config = await HC.apiRequest("/auth/google/config", { requireAuth: false });
  } catch {
    hint.textContent = "Unable to load Google login configuration from backend.";
    return;
  }

  if (!config.enabled || !config.google_client_id) {
    hint.textContent =
      "Google auth is disabled. Configure GOOGLE_CLIENT_ID, AUTH_SECRET_KEY, and an admin bootstrap email.";
    return;
  }

  hint.textContent = "Sign in with your managed Google account.";

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

  google.accounts.id.renderButton(document.getElementById("google-signin-host"), {
    type: "standard",
    shape: "pill",
    theme: "filled_blue",
    size: "large",
    text: "signin_with",
    width: 320,
  });
}

async function boot() {
  const restored = await HC.restoreSessionFromStorage();
  if (restored) {
    HC.redirectToRole(restored.session.user.role);
    return;
  }

  await initializeGoogleButton();
}

boot().catch((error) => {
  HC.showStatus(error.message || "Unable to initialize login.", "bad", 7000);
});
