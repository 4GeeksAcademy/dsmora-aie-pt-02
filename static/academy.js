const state = {
  className: null,
  type: null,
  file: null,
  catalog: [],
  sidebarOpen: true
};

const menuEl = document.getElementById("menu");
const contentEl = document.getElementById("content");
const metaClassEl = document.getElementById("meta-class");
const metaTypeEl = document.getElementById("meta-type");
const metaFileEl = document.getElementById("meta-file");
const menuToggleEl = document.getElementById("menu-toggle");
const menuOverlayEl = document.getElementById("menu-overlay");

function isMobile() {
  return window.matchMedia("(max-width: 960px)").matches;
}

function applySidebarState() {
  const mobile = isMobile();
  document.body.classList.toggle("menu-open", mobile && state.sidebarOpen);
  document.body.classList.toggle("sidebar-collapsed", !mobile && !state.sidebarOpen);

  if (menuToggleEl) {
    menuToggleEl.setAttribute("aria-expanded", String(state.sidebarOpen));
    menuToggleEl.setAttribute("aria-label", state.sidebarOpen ? "Ocultar panel" : "Mostrar panel");
  }
}

function setSidebarOpen(open) {
  state.sidebarOpen = open;
  applySidebarState();
}

function closeMenuIfMobile() {
  if (isMobile()) setSidebarOpen(false);
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function parseInlineMarkdown(text) {
  const codeChunks = [];
  let transformed = text.replace(/`([^`]+)`/g, (_, code) => {
    const idx = codeChunks.push(code) - 1;
    return `@@CODE${idx}@@`;
  });

  transformed = escapeHtml(transformed)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');

  transformed = transformed.replace(/@@CODE(\d+)@@/g, (_, idx) => {
    return `<code>${escapeHtml(codeChunks[Number(idx)])}</code>`;
  });

  return transformed;
}

function markdownToHtml(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  const html = [];
  let inCode = false;
  let inUl = false;
  let inOl = false;

  function closeLists() {
    if (inUl) {
      html.push("</ul>");
      inUl = false;
    }
    if (inOl) {
      html.push("</ol>");
      inOl = false;
    }
  }

  for (const line of lines) {
    if (line.startsWith("```")) {
      closeLists();
      if (!inCode) {
        html.push("<pre><code>");
        inCode = true;
      } else {
        html.push("</code></pre>");
        inCode = false;
      }
      continue;
    }

    if (inCode) {
      html.push(`${escapeHtml(line)}\n`);
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.*)$/);
    if (heading) {
      closeLists();
      const level = heading[1].length;
      html.push(`<h${level}>${parseInlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }

    const blockquote = line.match(/^>\s?(.*)$/);
    if (blockquote) {
      closeLists();
      html.push(`<blockquote>${parseInlineMarkdown(blockquote[1])}</blockquote>`);
      continue;
    }

    const ul = line.match(/^[-*]\s+(.*)$/);
    if (ul) {
      if (inOl) {
        html.push("</ol>");
        inOl = false;
      }
      if (!inUl) {
        html.push("<ul>");
        inUl = true;
      }
      html.push(`<li>${parseInlineMarkdown(ul[1])}</li>`);
      continue;
    }

    const ol = line.match(/^\d+\.\s+(.*)$/);
    if (ol) {
      if (inUl) {
        html.push("</ul>");
        inUl = false;
      }
      if (!inOl) {
        html.push("<ol>");
        inOl = true;
      }
      html.push(`<li>${parseInlineMarkdown(ol[1])}</li>`);
      continue;
    }

    if (/^\s*$/.test(line)) {
      closeLists();
      continue;
    }

    if (/^(-{3,}|\*{3,})$/.test(line.trim())) {
      closeLists();
      html.push("<hr />");
      continue;
    }

    closeLists();
    html.push(`<p>${parseInlineMarkdown(line)}</p>`);
  }

  closeLists();
  if (inCode) html.push("</code></pre>");
  return html.join("\n");
}

function setMeta() {
  metaClassEl.textContent = `Clase: ${state.className || "-"}`;
  metaTypeEl.textContent = `Tipo: ${state.type || "-"}`;
  metaFileEl.textContent = `Archivo: ${state.file || "-"}`;
}

function updateURL() {
  if (!state.className || !state.type || !state.file) return;

  const params = new URLSearchParams();
  params.set("class", state.className);
  params.set("type", state.type);
  params.set("file", state.file);
  history.replaceState({}, "", `${window.location.pathname}?${params.toString()}`);
}

async function loadCatalog() {
  // Static mode for GitHub Pages.
  try {
    const staticRes = await fetch("./catalog.json");
    if (staticRes.ok) {
      const staticPayload = await staticRes.json();
      if (Array.isArray(staticPayload.classes)) {
        return staticPayload.classes;
      }
    }
  } catch (_err) {
    // Ignore and fallback to API mode.
  }

  // Local Flask mode fallback.
  const apiRes = await fetch("/api/classes");
  if (!apiRes.ok) {
    return [];
  }
  const apiPayload = await apiRes.json();
  return apiPayload.classes || [];
}

async function loadContentPayload() {
  // Static mode for GitHub Pages.
  try {
    const fileRes = await fetch(`./${state.className}/${state.file}`);
    if (fileRes.ok) {
      const content = await fileRes.text();
      const extension = state.file.includes(".") ? state.file.split(".").pop().toLowerCase() : "";
      return { content, extension };
    }
  } catch (_err) {
    // Ignore and fallback to API mode.
  }

  // Local Flask mode fallback.
  const params = new URLSearchParams({
    class: state.className,
    type: state.type,
    file: state.file
  });

  const res = await fetch(`/api/content?${params.toString()}`);
  if (!res.ok) {
    return null;
  }

  const payload = await res.json();
  return {
    content: payload.content,
    extension: payload.extension
  };
}

async function loadContent() {
  if (!state.className || !state.type || !state.file) return;

  setMeta();
  contentEl.classList.remove("empty", "markdown", "raw");
  contentEl.textContent = "Cargando...";

  const payload = await loadContentPayload();
  if (!payload) {
    contentEl.classList.add("empty", "raw");
    contentEl.textContent = "No se pudo cargar el contenido solicitado.";
    return;
  }

  if (payload.extension === "md") {
    contentEl.classList.add("markdown");
    contentEl.innerHTML = markdownToHtml(payload.content);
  } else {
    contentEl.classList.add("raw");
    contentEl.textContent = payload.content;
  }

  updateURL();
  highlightActive();
}

function highlightActive() {
  document.querySelectorAll(".item").forEach((btn) => {
    const active = btn.dataset.class === state.className
      && btn.dataset.type === state.type
      && btn.dataset.file === state.file;
    btn.classList.toggle("active", active);
  });
}

function renderMenu() {
  menuEl.innerHTML = "";

  const lastIdx = state.catalog.length - 1;

  state.catalog.forEach((entry, idx) => {
    const block = document.createElement("section");
    block.className = `class-block${idx === lastIdx ? " open" : ""}`;

    const header = document.createElement("button");
    header.className = "class-header";
    header.textContent = entry.class;
    header.addEventListener("click", () => {
      block.classList.toggle("open");
    });

    const body = document.createElement("div");
    body.className = "class-body";

    const sumTitle = document.createElement("p");
    sumTitle.className = "section-title";
    sumTitle.textContent = "Resumenes";
    body.appendChild(sumTitle);

    if (entry.summaries.length === 0) {
      const empty = document.createElement("p");
      empty.className = "empty";
      empty.textContent = "Sin resumenes";
      body.appendChild(empty);
    } else {
      entry.summaries.forEach((file) => {
        const btn = document.createElement("button");
        btn.className = "item";
        btn.textContent = file;
        btn.dataset.class = entry.class;
        btn.dataset.type = "resumen";
        btn.dataset.file = file;
        btn.addEventListener("click", () => {
          state.className = entry.class;
          state.type = "resumen";
          state.file = file;
          loadContent();
          closeMenuIfMobile();
        });
        body.appendChild(btn);
      });
    }

    block.appendChild(header);
    block.appendChild(body);
    menuEl.appendChild(block);
  });
}

function pickDefaultSummary(summaries) {
  const resume = summaries.find((file) => /^resume/i.test(file) || /^resumen/i.test(file));
  return resume || summaries[0];
}

function pickInitialSelection() {
  const params = new URLSearchParams(window.location.search);
  const qClass = params.get("class");
  const qType = params.get("type");
  const qFile = params.get("file");

  if (qClass && (qType === "resumen" || qType === "completa") && qFile) {
    state.className = qClass;
    state.type = qType;
    state.file = qFile;
    return;
  }

  for (let i = state.catalog.length - 1; i >= 0; i--) {
    const entry = state.catalog[i];
    if (entry.summaries.length > 0) {
      state.className = entry.class;
      state.type = "resumen";
      state.file = pickDefaultSummary(entry.summaries);
      return;
    }
  }
}

async function bootstrap() {
  let wasMobile = isMobile();
  state.sidebarOpen = !wasMobile;

  if (menuToggleEl) {
    menuToggleEl.addEventListener("click", () => {
      setSidebarOpen(!state.sidebarOpen);
    });
  }

  if (menuOverlayEl) {
    menuOverlayEl.addEventListener("click", () => {
      setSidebarOpen(false);
    });
  }

  window.addEventListener("resize", () => {
    const mobileNow = isMobile();
    if (mobileNow !== wasMobile) {
      state.sidebarOpen = !mobileNow;
      wasMobile = mobileNow;
    }
    applySidebarState();
  });

  applySidebarState();
  state.catalog = await loadCatalog();
  renderMenu();
  pickInitialSelection();
  setMeta();
  loadContent();
}

bootstrap();
