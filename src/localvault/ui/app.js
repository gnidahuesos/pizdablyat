const statusEl = document.getElementById("status");
const encryptOutput = document.getElementById("encrypt-output");
const decryptOutput = document.getElementById("decrypt-output");

const setStatus = (message, tone = "info") => {
  statusEl.textContent = message;
  statusEl.dataset.tone = tone;
};

const postJson = async (url, body) => {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  return response.json();
};

const initForm = document.getElementById("init-form");
initForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(initForm);
  const spaces = data.get("spaces").split(",").map((space) => space.trim()).filter(Boolean);

  try {
    setStatus("Initializing workspace...", "info");
    const response = await postJson("/api/init", {
      path: data.get("path"),
      passphrase: data.get("passphrase"),
      spaces,
    });
    setStatus(`Workspace ready at ${response.path}`, "success");
  } catch (error) {
    setStatus(`Init failed: ${error.message}`, "error");
  }
});

const encryptForm = document.getElementById("encrypt-form");
encryptForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(encryptForm);

  try {
    setStatus("Encrypting text...", "info");
    const response = await postJson("/api/encrypt", {
      passphrase: data.get("passphrase"),
      plaintext: data.get("plaintext"),
    });
    encryptOutput.value = response.payload;
    setStatus("Encryption complete.", "success");
  } catch (error) {
    setStatus(`Encrypt failed: ${error.message}`, "error");
  }
});

const decryptForm = document.getElementById("decrypt-form");
decryptForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const data = new FormData(decryptForm);

  try {
    setStatus("Decrypting payload...", "info");
    const response = await postJson("/api/decrypt", {
      passphrase: data.get("passphrase"),
      payload: data.get("payload"),
    });
    decryptOutput.value = response.plaintext;
    setStatus("Decryption complete.", "success");
  } catch (error) {
    setStatus(`Decrypt failed: ${error.message}`, "error");
  }
});
