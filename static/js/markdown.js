const MarkdownRenderer = {
  initialized: false,

  init() {
    if (this.initialized) return;

    // Configure marked
    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
      },
      breaks: true,
      gfm: true,
    });

    // Initialize mermaid
    mermaid.initialize({
      startOnLoad: false,
      theme: ThemeManager.get() === 'dark' ? 'dark' : 'default',
      securityLevel: 'loose',
    });

    // Re-init mermaid on theme change
    document.addEventListener('themechange', (e) => {
      mermaid.initialize({
        startOnLoad: false,
        theme: e.detail.theme === 'dark' ? 'dark' : 'default',
        securityLevel: 'loose',
      });
    });

    this.initialized = true;
  },

  async render(markdown, container) {
    this.init();

    // Parse markdown to HTML
    const html = marked.parse(markdown);
    container.innerHTML = html;

    // Process mermaid code blocks
    // After marked.js parses ```mermaid blocks, they become <pre><code class="language-mermaid">
    const mermaidBlocks = container.querySelectorAll('pre code.language-mermaid');
    for (let i = 0; i < mermaidBlocks.length; i++) {
      const block = mermaidBlocks[i];
      const pre = block.parentElement;
      const mermaidCode = block.textContent;

      const div = document.createElement('div');
      div.className = 'mermaid';
      div.textContent = mermaidCode;
      pre.replaceWith(div);
    }

    // Render all mermaid diagrams
    if (container.querySelectorAll('.mermaid').length > 0) {
      await mermaid.run({ nodes: container.querySelectorAll('.mermaid') });
    }

    // Apply highlight.js to remaining code blocks
    container.querySelectorAll('pre code:not(.language-mermaid)').forEach((block) => {
      hljs.highlightElement(block);
    });
  }
};

window.MarkdownRenderer = MarkdownRenderer;
