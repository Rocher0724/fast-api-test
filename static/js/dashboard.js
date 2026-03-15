const Dashboard = {
  currentCategory: null,
  authToken: null,  // stored after login

  init() {
    this.renderCategories();
    this.setupTabs();
    this.setupMobile();

    // Select first category by default
    if (APP_CONFIG.CATEGORIES.length > 0) {
      this.selectCategory(APP_CONFIG.CATEGORIES[0].id);
    }
  },

  renderCategories() {
    const nav = document.getElementById('categoryNav');
    const drawerNav = document.getElementById('drawerCategoryNav');

    const html = APP_CONFIG.CATEGORIES.map(cat => `
      <a class="sidebar-item" data-category="${cat.id}" onclick="Dashboard.selectCategory('${cat.id}')">
        <span class="cat-icon">${cat.icon}</span>
        <span class="cat-name">${cat.name}</span>
        <span class="cat-count">${cat.count}</span>
      </a>
    `).join('');

    nav.innerHTML = html;
    if (drawerNav) drawerNav.innerHTML = html;
  },

  selectCategory(categoryId) {
    this.currentCategory = categoryId;
    const cat = APP_CONFIG.getCategoryById(categoryId);

    // Update sidebar active state
    document.querySelectorAll('[data-category]').forEach(el => {
      el.classList.toggle('active', el.dataset.category === categoryId);
    });

    // Update header
    document.getElementById('categoryTitle').textContent = `${cat.icon} ${cat.name}`;

    // Render endpoints
    const endpoints = APP_CONFIG.getEndpointsByCategory(categoryId);
    document.getElementById('endpointCount').textContent = `${endpoints.length}개`;
    this.renderEndpoints(endpoints);

    // Close mobile drawer
    this.closeDrawer();
  },

  renderEndpoints(endpoints) {
    const list = document.getElementById('endpointList');

    list.innerHTML = endpoints.map((ep, i) => {
      const methodClass = `badge-${ep.method.toLowerCase()}`;
      const hasBody = ep.body || ep.rawBody;

      return `
        <div class="endpoint-card" data-index="${i}">
          <div class="endpoint-header">
            <span class="badge ${methodClass}">${ep.method}</span>
            <code class="endpoint-path">${ep.path}</code>
          </div>
          <p class="endpoint-desc">${ep.description}</p>
          ${hasBody ? `
            <div class="endpoint-body">
              <label>Request Body:</label>
              <textarea class="body-editor" id="body-${i}" rows="3">${
                ep.rawBody || JSON.stringify(ep.body, null, 2)
              }</textarea>
            </div>
          ` : ''}
          <div class="endpoint-actions">
            <button class="btn btn-primary btn-small" onclick="Dashboard.executeEndpoint(${i})">
              실행
            </button>
            ${ep.requiresAuth ? '<span class="auth-badge">🔐 인증 필요</span>' : ''}
          </div>
        </div>
      `;
    }).join('');
  },

  async executeEndpoint(index) {
    const endpoints = APP_CONFIG.getEndpointsByCategory(this.currentCategory);
    const ep = endpoints[index];

    const startTime = performance.now();

    // Build request
    const options = {
      method: ep.method,
      headers: {},
    };

    // Add auth token if available
    if (this.authToken) {
      options.headers['Authorization'] = `Bearer ${this.authToken}`;
    }

    // Add body for POST endpoints
    if (ep.method === 'POST') {
      if (ep.rawBody) {
        options.body = ep.rawBody;
        options.headers['Content-Type'] = ep.contentType || 'application/json';
      } else if (ep.body) {
        const bodyEditor = document.getElementById(`body-${index}`);
        const bodyText = bodyEditor ? bodyEditor.value : JSON.stringify(ep.body);
        try {
          options.body = bodyText;
          options.headers['Content-Type'] = ep.contentType || 'application/json';
        } catch (e) {
          options.body = bodyText;
        }
      }
    }

    // Add custom content type if specified
    if (ep.contentType) {
      options.headers['Content-Type'] = ep.contentType;
    }

    try {
      const response = await fetch(ep.path, options);
      const elapsed = Math.round(performance.now() - startTime);

      let responseBody;
      const contentType = response.headers.get('content-type') || '';
      if (contentType.includes('application/json')) {
        responseBody = await response.json();
      } else {
        responseBody = await response.text();
      }

      // Check if this is a login response — store token
      if (ep.path.includes('/auth/login') && response.ok && responseBody.token) {
        this.authToken = responseBody.token;
        document.getElementById('authStatus').textContent = `토큰: ${this.authToken.substring(0, 20)}...`;
        document.getElementById('authStatus').classList.add('auth-active');
      }

      // Display response
      this.showResponse(response, responseBody, elapsed, ep, options);

    } catch (err) {
      this.showError(err);
    }
  },

  showResponse(response, body, elapsed, endpoint, requestOptions) {
    // Response tab
    const statusClass = `status-${Math.floor(response.status / 100)}xx`;
    const responseTab = document.getElementById('tabResponse');
    responseTab.innerHTML = `
      <div class="response-meta">
        <span class="response-status ${statusClass}">${response.status} ${response.statusText}</span>
        <span class="response-time">${elapsed}ms</span>
      </div>
      <div class="response-headers">
        <strong>응답 헤더:</strong>
        <pre class="code-block">${this.formatHeaders(response.headers)}</pre>
      </div>
      <div class="response-body">
        <strong>응답 본문:</strong>
        <pre class="code-block"><code class="language-json">${
          typeof body === 'string' ? this.escapeHtml(body) : JSON.stringify(body, null, 2)
        }</code></pre>
      </div>
    `;

    // Highlight code
    responseTab.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));

    // Request tab
    const requestTab = document.getElementById('tabRequest');
    requestTab.innerHTML = `
      <div class="request-info">
        <div class="request-method">
          <span class="badge badge-${endpoint.method.toLowerCase()}">${endpoint.method}</span>
          <code>${endpoint.path}</code>
        </div>
        <div class="request-headers">
          <strong>요청 헤더:</strong>
          <pre class="code-block">${this.formatRequestHeaders(requestOptions.headers)}</pre>
        </div>
        ${requestOptions.body ? `
          <div class="request-body">
            <strong>요청 본문:</strong>
            <pre class="code-block"><code class="language-json">${this.escapeHtml(requestOptions.body)}</code></pre>
          </div>
        ` : ''}
      </div>
    `;
    requestTab.querySelectorAll('pre code').forEach(block => hljs.highlightElement(block));

    // Learning tab
    const learningTab = document.getElementById('tabLearning');
    const devtoolsHint = APP_CONFIG.DEVTOOLS_HINTS[endpoint.devtools] || '';
    const chapter = APP_CONFIG.CHAPTER_MAP[endpoint.chapterLink];

    // Extract lesson from response body
    let lessonHtml = '';
    if (body && typeof body === 'object') {
      if (body.lesson) lessonHtml = `<div class="learning-lesson"><h4>💡 학습 포인트</h4><p>${body.lesson}</p></div>`;
      if (body.checklist) lessonHtml += `<div class="learning-checklist"><h4>✅ 체크리스트</h4><ul>${body.checklist.map(c => `<li>${c}</li>`).join('')}</ul></div>`;
      if (body.hint) lessonHtml += `<div class="learning-hint"><p>💡 ${body.hint}</p></div>`;
    }

    learningTab.innerHTML = `
      <div class="learning-content">
        ${lessonHtml}
        <div class="learning-devtools">
          <h4>🔍 확인 장소</h4>
          <p>${devtoolsHint}</p>
        </div>
        ${chapter ? `
          <div class="learning-chapter">
            <h4>📖 관련 강의</h4>
            <a href="/lecture#chapter=${encodeURIComponent(chapter.file.replace('.md', ''))}" class="btn btn-secondary btn-small">
              ${chapter.title} 챕터로 이동
            </a>
          </div>
        ` : ''}
      </div>
    `;

    // Activate response tab
    this.switchTab('response');
  },

  showError(error) {
    const responseTab = document.getElementById('tabResponse');
    responseTab.innerHTML = `
      <div class="response-error">
        <span class="response-status status-5xx">네트워크 에러</span>
        <p>${error.message}</p>
        <p class="hint">CORS 에러인 경우 브라우저 Console 탭을 확인하세요.</p>
      </div>
    `;
    this.switchTab('response');
  },

  // Tab management
  setupTabs() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
    });
  },

  switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabId);
    });
    document.querySelectorAll('.tab-pane').forEach(pane => {
      pane.classList.toggle('active', pane.id === `tab${tabId.charAt(0).toUpperCase() + tabId.slice(1)}`);
    });
  },

  // Helper methods
  formatHeaders(headers) {
    let result = '';
    headers.forEach((value, key) => { result += `${key}: ${value}\n`; });
    return result || '(없음)';
  },

  formatRequestHeaders(headers) {
    return Object.entries(headers).map(([k, v]) => `${k}: ${v}`).join('\n') || '(없음)';
  },

  escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  },

  // Mobile
  setupMobile() {
    document.getElementById('menuToggle')?.addEventListener('click', () => this.toggleDrawer());
    document.getElementById('drawerOverlay')?.addEventListener('click', () => this.closeDrawer());
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

document.addEventListener('DOMContentLoaded', () => Dashboard.init());
window.Dashboard = Dashboard;
