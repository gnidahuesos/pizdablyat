import { useMemo, useState } from "react";

const sampleStats = [
  { label: "Encrypted pages", value: "1,248" },
  { label: "Backlinks", value: "9,532" },
  { label: "Spaces", value: "3" },
];

const features = [
  "Local-first storage with encrypted vaults",
  "Block-based editor with stable IDs",
  "Markdown-friendly pages and backlinks",
  "Cross-platform desktop shell (macOS + Windows)",
];

export default function App() {
  const [passphrase, setPassphrase] = useState("");
  const [workspacePath, setWorkspacePath] = useState("~/LocalVault");
  const [spaces, setSpaces] = useState("personal, work");
  const [status, setStatus] = useState("Ready to initialize your encrypted workspace.");
  const [plaintext, setPlaintext] = useState("");
  const [payload, setPayload] = useState("");

  const spaceList = useMemo(
    () => spaces.split(",").map((space) => space.trim()).filter(Boolean),
    [spaces]
  );

  const handleInit = (event) => {
    event.preventDefault();
    setStatus(`Workspace will be created at ${workspacePath} with ${spaceList.length} space(s).`);
  };

  const handleEncrypt = (event) => {
    event.preventDefault();
    setStatus("Encryption queued for the desktop engine.");
    setPayload(plaintext ? `ENCRYPTED:${btoa(plaintext).slice(0, 64)}...` : "");
  };

  const handleDecrypt = (event) => {
    event.preventDefault();
    setStatus("Decryption queued for the desktop engine.");
    if (payload.startsWith("ENCRYPTED:")) {
      setPlaintext("Decrypted content will appear here once the engine is connected.");
    }
  };

  return (
    <div className="app">
      <div className="orb orb-a" />
      <div className="orb orb-b" />
      <div className="orb orb-c" />

      <header className="hero">
        <div>
          <p className="eyebrow">Local-first • Encrypted • Cross-platform</p>
          <h1>LocalVault Desktop</h1>
          <p className="subtitle">
            A glassmorphism React shell inspired by iOS 26. Designed for a native desktop wrapper (Tauri/Electron).
          </p>
        </div>
        <div className="glass-card">
          <h2>Status</h2>
          <p>{status}</p>
          <div className="chips">
            {sampleStats.map((stat) => (
              <div key={stat.label} className="chip">
                <span>{stat.value}</span>
                <small>{stat.label}</small>
              </div>
            ))}
          </div>
        </div>
      </header>

      <section className="grid">
        <article className="glass-card">
          <h3>Workspace Setup</h3>
          <p>Provision a new encrypted vault on your local filesystem.</p>
          <form onSubmit={handleInit}>
            <label>
              Workspace path
              <input value={workspacePath} onChange={(event) => setWorkspacePath(event.target.value)} />
            </label>
            <label>
              Passphrase
              <input
                type="password"
                value={passphrase}
                onChange={(event) => setPassphrase(event.target.value)}
              />
            </label>
            <label>
              Spaces
              <input value={spaces} onChange={(event) => setSpaces(event.target.value)} />
            </label>
            <button type="submit">Initialize</button>
          </form>
        </article>

        <article className="glass-card">
          <h3>Encrypt</h3>
          <p>Encrypt plaintext locally and store it in the vault.</p>
          <form onSubmit={handleEncrypt}>
            <label>
              Passphrase
              <input
                type="password"
                value={passphrase}
                onChange={(event) => setPassphrase(event.target.value)}
              />
            </label>
            <label>
              Plaintext
              <textarea value={plaintext} onChange={(event) => setPlaintext(event.target.value)} rows={6} />
            </label>
            <button type="submit">Encrypt</button>
          </form>
        </article>

        <article className="glass-card">
          <h3>Decrypt</h3>
          <p>Paste encrypted payloads to preview decrypted content.</p>
          <form onSubmit={handleDecrypt}>
            <label>
              Payload
              <textarea value={payload} onChange={(event) => setPayload(event.target.value)} rows={6} />
            </label>
            <button type="submit">Decrypt</button>
          </form>
        </article>
      </section>

      <section className="glass-card wide">
        <h3>Desktop-first roadmap</h3>
        <ul>
          {features.map((feature) => (
            <li key={feature}>{feature}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
