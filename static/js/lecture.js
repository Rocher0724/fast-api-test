const LectureViewer = {
  lectures: [],        // from /api/lectures
  currentIndex: -1,    // current lecture index

  async init() {
    // 1. Fetch lecture list from /api/lectures
    const res = await fetch('/api/lectures');
    this.lectures = await res.json();

    // 2. Render sidebar with chapter list
    this.renderSidebar();

    // 3. Check URL hash for initial chapter
    const hash = window.location.hash;
    if (hash && hash.startsWith('#chapter=')) {
      const chapterStem = decodeURIComponent(hash.replace('#chapter=', ''));
      const idx = this.lectures.findIndex(l => l.stem === chapterStem);
      if (idx >= 0) {
        this.loadChapter(idx);
        return;
      }
    }

    // 4. Default: load first chapter (00-목차)
    if (this.lectures.length > 0) {
      this.loadChapter(0);
    }

    // 5. Set up event listeners
    document.getElementById('prevBtn').addEventListener('click', () => this.prev());
    document.getElementById('nextBtn').addEventListener('click', () => this.next());
    window.addEventListener('hashchange', () => this.onHashChange());

    // 6. Set up mobile menu
    document.getElementById('menuToggle')?.addEventListener('click', () => this.toggleDrawer());
    document.getElementById('drawerOverlay')?.addEventListener('click', () => this.closeDrawer());

    // 7. Scroll progress tracking
    window.addEventListener('scroll', () => this.updateProgress());

    // 8. Keyboard navigation: left/right arrow keys
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') this.prev();
      if (e.key === 'ArrowRight') this.next();
    });
  },

  renderSidebar() {
    const sidebarNav = document.getElementById('sidebarNav');
    const drawerNav = document.getElementById('drawerNav');

    // Group: chapters (numbered) and appendices
    let html = '';
    this.lectures.forEach((lecture, index) => {
      const displayTitle = this.formatTitle(lecture);
      html += `<a class="sidebar-item" data-index="${index}" onclick="LectureViewer.loadChapter(${index})">${displayTitle}</a>`;
    });

    sidebarNav.innerHTML = html;
    if (drawerNav) drawerNav.innerHTML = html;
  },

  formatTitle(lecture) {
    // Format like "0. 목차", "1. 에러는 어디에서 나는가", "부록 A. 에러 사전"
    const stem = lecture.stem;
    if (stem.startsWith('appendix-')) {
      const letter = stem.replace('appendix-', '').charAt(0).toUpperCase();
      return `부록 ${letter}. ${lecture.title}`;
    }
    const num = stem.split('-')[0];
    return `${num}. ${lecture.title}`;
  },

  async loadChapter(index) {
    if (index < 0 || index >= this.lectures.length) return;

    this.currentIndex = index;
    const lecture = this.lectures[index];

    // Update URL hash (without triggering hashchange reload)
    history.replaceState(null, '', `#chapter=${encodeURIComponent(lecture.stem)}`);

    // Update sidebar active state
    document.querySelectorAll('.sidebar-item').forEach((item) => {
      item.classList.toggle('active', parseInt(item.dataset.index) === index);
    });

    // Show loading state
    const content = document.getElementById('lectureContent');
    content.innerHTML = '<div class="lecture-loading">강의를 불러오는 중...</div>';

    // Fetch and render markdown
    try {
      const res = await fetch(`/api/lectures/${lecture.filename}`);
      const markdown = await res.text();
      await MarkdownRenderer.render(markdown, content);
    } catch (err) {
      content.innerHTML = `<div class="lecture-error">강의를 불러오지 못했습니다: ${err.message}</div>`;
    }

    // Update prev/next buttons
    this.updateNav();

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Close drawer if open (mobile)
    this.closeDrawer();
  },

  updateNav() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const navInfo = document.getElementById('navInfo');

    prevBtn.disabled = this.currentIndex <= 0;
    nextBtn.disabled = this.currentIndex >= this.lectures.length - 1;
    navInfo.textContent = `${this.currentIndex + 1} / ${this.lectures.length}`;
  },

  prev() { if (this.currentIndex > 0) this.loadChapter(this.currentIndex - 1); },
  next() { if (this.currentIndex < this.lectures.length - 1) this.loadChapter(this.currentIndex + 1); },

  onHashChange() {
    const hash = window.location.hash;
    if (hash.startsWith('#chapter=')) {
      const stem = decodeURIComponent(hash.replace('#chapter=', ''));
      const idx = this.lectures.findIndex(l => l.stem === stem);
      if (idx >= 0 && idx !== this.currentIndex) this.loadChapter(idx);
    }
  },

  updateProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    const fill = document.getElementById('progressFill');
    if (fill) fill.style.width = `${Math.min(progress, 100)}%`;
  },

  toggleDrawer() {
    document.getElementById('drawer')?.classList.toggle('active');
    document.getElementById('drawerOverlay')?.classList.toggle('active');
  },

  closeDrawer() {
    document.getElementById('drawer')?.classList.remove('active');
    document.getElementById('drawerOverlay')?.classList.remove('active');
  }
};

document.addEventListener('DOMContentLoaded', () => LectureViewer.init());
window.LectureViewer = LectureViewer;
