const DataflowViewer = {
  diagrams: [],  // Array of mermaid code strings
  currentTab: 0,

  async init() {
    // Initialize mermaid
    mermaid.initialize({
      startOnLoad: false,
      theme: ThemeManager.get() === 'dark' ? 'dark' : 'default',
      securityLevel: 'loose',
    });

    // Listen for theme changes to re-render
    document.addEventListener('themechange', (e) => {
      mermaid.initialize({
        startOnLoad: false,
        theme: e.detail.theme === 'dark' ? 'dark' : 'default',
        securityLevel: 'loose',
      });
      this.renderCurrentDiagram();
    });

    // Fetch the data flow markdown
    try {
      const res = await fetch('/api/lectures/00-데이터-플로우.md');
      const markdown = await res.text();
      this.parseDiagrams(markdown);
    } catch (err) {
      console.error('Failed to load data flow diagrams:', err);
    }

    // Set up tab switching
    document.querySelectorAll('#diagramTabs .tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = parseInt(btn.dataset.diagram);
        this.switchTab(idx);
      });
    });

    // Render first diagram
    if (this.diagrams.length > 0) {
      await this.renderDiagram(0);
    }
  },

  parseDiagrams(markdown) {
    // Extract all ```mermaid blocks
    const regex = /```mermaid\n([\s\S]*?)```/g;
    let match;
    while ((match = regex.exec(markdown)) !== null) {
      this.diagrams.push(match[1].trim());
    }
  },

  async switchTab(index) {
    this.currentTab = index;

    // Update tab buttons
    document.querySelectorAll('#diagramTabs .tab-btn').forEach(btn => {
      btn.classList.toggle('active', parseInt(btn.dataset.diagram) === index);
    });

    // Update tab panes
    document.querySelectorAll('#diagramContent .tab-pane').forEach((pane, i) => {
      pane.classList.toggle('active', i === index);
    });

    // Render diagram if not already rendered
    await this.renderDiagram(index);
  },

  async renderDiagram(index) {
    if (!this.diagrams[index]) return;

    const container = document.getElementById(`mermaid-${index}`);
    if (!container) return;

    // Clear and re-render
    container.innerHTML = '';
    container.textContent = this.diagrams[index];
    container.removeAttribute('data-processed');

    try {
      await mermaid.run({ nodes: [container] });
    } catch (err) {
      console.error(`Mermaid render error for diagram ${index}:`, err);
      container.innerHTML = `<p style="color: var(--color-error);">다이어그램 렌더링 실패: ${err.message}</p>`;
    }
  },

  async renderCurrentDiagram() {
    await this.renderDiagram(this.currentTab);
  }
};

document.addEventListener('DOMContentLoaded', () => DataflowViewer.init());
window.DataflowViewer = DataflowViewer;
