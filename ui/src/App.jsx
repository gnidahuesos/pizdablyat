import { useMemo, useState } from "react";

const blockTypes = [
  { id: "text", label: "Text" },
  { id: "heading", label: "Heading" },
  { id: "list", label: "List item" },
  { id: "quote", label: "Quote" },
  { id: "code", label: "Code block" },
];

const initialPages = [
  {
    id: "page-1",
    title: "Welcome",
    blocks: [
      { id: "b1", type: "heading", text: "LocalVault" },
      { id: "b2", type: "text", text: "A local-first workspace with encrypted storage." },
      { id: "b3", type: "text", text: "Try typing / for commands or [[ to link." },
    ],
  },
  {
    id: "page-2",
    title: "Project Roadmap",
    blocks: [
      { id: "b4", type: "heading", text: "Roadmap" },
      { id: "b5", type: "list", text: "Offline-first editor" },
      { id: "b6", type: "list", text: "Encrypted attachments" },
    ],
  },
];

const createPage = (title) => ({
  id: `page-${crypto.randomUUID()}`,
  title,
  blocks: [{ id: `b-${crypto.randomUUID()}`, type: "text", text: "" }],
});

const parseLinkQuery = (text) => {
  const match = text.match(/\[\[([^\]]*)$/);
  return match ? match[1] : null;
};

const replaceLinkQuery = (text, pageTitle) => {
  return text.replace(/\[\[[^\]]*$/, `[[${pageTitle}]]`);
};

const renderLinkedText = (text, onNavigate) => {
  const parts = text.split(/(\[\[[^\]]+\]\])/g);
  return parts.map((part, index) => {
    const match = part.match(/^\[\[([^\]]+)\]\]$/);
    if (match) {
      return (
        <button
          key={`${part}-${index}`}
          type="button"
          className="link-pill"
          onClick={() => onNavigate(match[1])}
        >
          {match[1]}
        </button>
      );
    }
    return <span key={`${part}-${index}`}>{part}</span>;
  });
};

export default function App() {
  const [pages, setPages] = useState(initialPages);
  const [activePageId, setActivePageId] = useState(initialPages[0].id);
  const [search, setSearch] = useState("");
  const [slashMenu, setSlashMenu] = useState(null);
  const [linkMenu, setLinkMenu] = useState(null);
  const [status, setStatus] = useState("Ready. Create links with [[ and blocks with /.");

  const activePage = pages.find((page) => page.id === activePageId) ?? pages[0];

  const filteredPages = useMemo(() => {
    return pages.filter((page) => page.title.toLowerCase().includes(search.toLowerCase()));
  }, [pages, search]);

  const updateBlock = (blockId, updater) => {
    setPages((prev) =>
      prev.map((page) =>
        page.id === activePageId
          ? {
              ...page,
              blocks: page.blocks.map((block) =>
                block.id === blockId ? { ...block, ...updater(block) } : block
              ),
            }
          : page
      )
    );
  };

  const handleTextChange = (blockId, value) => {
    let newType = null;
    let newValue = value;

    if (value.startsWith("# ")) {
      newType = "heading";
      newValue = value.slice(2);
    } else if (value.startsWith("- ")) {
      newType = "list";
      newValue = value.slice(2);
    }

    updateBlock(blockId, () => ({ text: newValue, ...(newType ? { type: newType } : {}) }));

    if (value.endsWith("/")) {
      setSlashMenu({ blockId });
    }

    const query = parseLinkQuery(value);
    if (query !== null) {
      setLinkMenu({ blockId, query });
    } else if (linkMenu?.blockId === blockId) {
      setLinkMenu(null);
    }
  };

  const applyBlockType = (blockId, type) => {
    updateBlock(blockId, () => ({ type, text: "" }));
    setSlashMenu(null);
    setStatus(`Inserted ${type} block.`);
  };

  const insertLink = (blockId, title) => {
    updateBlock(blockId, (block) => ({ text: replaceLinkQuery(block.text, title) }));
    setLinkMenu(null);
    setStatus(`Linked to ${title}.`);
  };

  const createNewPage = () => {
    const title = `Untitled ${pages.length + 1}`;
    const page = createPage(title);
    setPages((prev) => [page, ...prev]);
    setActivePageId(page.id);
    setStatus(`Created ${title}.`);
  };

  const navigateToTitle = (title) => {
    const match = pages.find((page) => page.title === title);
    if (match) {
      setActivePageId(match.id);
      setStatus(`Navigated to ${title}.`);
    }
  };

  const filteredLinkTargets = pages.filter((page) =>
    page.title.toLowerCase().includes((linkMenu?.query ?? "").toLowerCase())
  );

  return (
    <div className="app">
      <div className="orb orb-a" />
      <div className="orb orb-b" />
      <div className="orb orb-c" />

      <aside className="sidebar glass-card">
        <div className="sidebar-header">
          <h2>LocalVault</h2>
          <button type="button" onClick={createNewPage}>
            + New Page
          </button>
        </div>
        <input
          className="search"
          placeholder="Search pages"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <nav className="page-list">
          {filteredPages.map((page) => (
            <button
              key={page.id}
              type="button"
              className={`page-item ${page.id === activePageId ? "active" : ""}`}
              onClick={() => setActivePageId(page.id)}
            >
              {page.title}
            </button>
          ))}
        </nav>
      </aside>

      <main className="main">
        <header className="hero glass-card">
          <div>
            <p className="eyebrow">Local-first • Encrypted • Cross-platform</p>
            <h1>{activePage.title}</h1>
            <p className="subtitle">
              Glassmorphism React desktop shell. Use / for block commands, [[ for links, # for headings, - for lists.
            </p>
          </div>
          <div className="status">
            <h3>Status</h3>
            <p>{status}</p>
          </div>
        </header>

        <section className="editor-grid">
          <article className="glass-card editor">
            <h3>Block Editor</h3>
            <div className="blocks">
              {activePage.blocks.map((block) => (
                <div key={block.id} className={`block block-${block.type}`}>
                  <textarea
                    rows={block.type === "code" ? 4 : 2}
                    placeholder="Type here..."
                    value={block.text}
                    onChange={(event) => handleTextChange(block.id, event.target.value)}
                  />
                  {slashMenu?.blockId === block.id && (
                    <div className="menu">
                      {blockTypes.map((type) => (
                        <button key={type.id} type="button" onClick={() => applyBlockType(block.id, type.id)}>
                          {type.label}
                        </button>
                      ))}
                    </div>
                  )}
                  {linkMenu?.blockId === block.id && (
                    <div className="menu">
                      {filteredLinkTargets.length === 0 ? (
                        <span className="menu-empty">No matches</span>
                      ) : (
                        filteredLinkTargets.map((page) => (
                          <button key={page.id} type="button" onClick={() => insertLink(block.id, page.title)}>
                            {page.title}
                          </button>
                        ))
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </article>

          <article className="glass-card preview">
            <h3>Preview</h3>
            <div className="preview-body">
              {activePage.blocks.map((block) => (
                <div key={block.id} className={`preview-line ${block.type}`}>
                  {block.type === "heading" && <h2>{block.text || "Heading"}</h2>}
                  {block.type === "list" && (
                    <div className="list-item">
                      <span>•</span>
                      <p>{renderLinkedText(block.text || "List item", navigateToTitle)}</p>
                    </div>
                  )}
                  {block.type === "quote" && <blockquote>{renderLinkedText(block.text || "Quote", navigateToTitle)}</blockquote>}
                  {block.type === "code" && <pre>{block.text || "code"}</pre>}
                  {block.type === "text" && <p>{renderLinkedText(block.text || "Paragraph", navigateToTitle)}</p>}
                </div>
              ))}
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}
