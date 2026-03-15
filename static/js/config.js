const APP_CONFIG = {
  API_BASE: '',  // same origin

  CATEGORIES: [
    { id: 'http', name: 'HTTP 상태 코드', prefix: '/errors/http', icon: '🌐', description: 'HTTP 상태 코드별 에러 응답', count: 12 },
    { id: 'validation', name: '유효성 검사', prefix: '/errors/validation', icon: '✅', description: 'Pydantic 유효성 검사 에러', count: 9 },
    { id: 'database', name: 'DB 시뮬레이션', prefix: '/errors/database', icon: '🗄️', description: '데이터베이스 에러 시뮬레이션', count: 10 },
    { id: 'auth', name: '인증/인가', prefix: '/errors/auth', icon: '🔐', description: '인증 토큰과 권한 에러', count: 6 },
    { id: 'logic', name: '비즈니스 로직', prefix: '/errors/logic', icon: '⚙️', description: 'Python 런타임 에러', count: 10 },
    { id: 'cors', name: 'CORS', prefix: '/errors/cors', icon: '🔒', description: 'Cross-Origin 요청 에러', count: 6 },
    { id: 'request', name: '요청/응답', prefix: '/errors/request', icon: '📡', description: 'HTTP 요청/응답 형식 에러', count: 9 },
    { id: 'async', name: '비동기', prefix: '/errors/async', icon: '⏱️', description: 'asyncio 비동기 에러', count: 5 },
    { id: 'file', name: '파일/리소스', prefix: '/errors/file', icon: '📁', description: '파일 시스템 에러', count: 5 },
  ],

  ENDPOINTS: [
    // === HTTP 상태 코드 (12) ===
    { category: 'http', method: 'GET', path: '/errors/http/400', description: '400 Bad Request — 클라이언트 요청 오류', devtools: 'Network', chapterLink: '01' },
    { category: 'http', method: 'GET', path: '/errors/http/401', description: '401 Unauthorized — 인증 필요 (WWW-Authenticate 헤더)', devtools: 'Network', chapterLink: '01' },
    { category: 'http', method: 'GET', path: '/errors/http/403', description: '403 Forbidden — 인증됐지만 권한 없음', devtools: 'Network', chapterLink: '01' },
    { category: 'http', method: 'GET', path: '/errors/http/404', description: '404 Not Found — 리소스 없음', devtools: 'Network', chapterLink: '01' },
    { category: 'http', method: 'POST', path: '/errors/http/405', description: '405 Method Not Allowed — GET으로 호출하면 405 발생', devtools: 'Network', chapterLink: '01', body: {} },
    { category: 'http', method: 'GET', path: '/errors/http/408', description: '408 Request Timeout — 요청 타임아웃', devtools: 'Network', chapterLink: '01' },
    { category: 'http', method: 'POST', path: '/errors/http/409', description: '409 Conflict — 중복 리소스 (username 충돌)', devtools: 'Network', chapterLink: '01', body: { username: 'existing_user' } },
    { category: 'http', method: 'POST', path: '/errors/http/422', description: '422 Unprocessable Entity — Pydantic 자동 유효성 검사', devtools: 'Network', chapterLink: '01', body: { name: 'test' } },
    { category: 'http', method: 'GET', path: '/errors/http/429', description: '429 Too Many Requests — Rate Limiting (3회 초과 시 차단)', devtools: 'Network', chapterLink: '01' },
    { category: 'http', method: 'GET', path: '/errors/http/500', description: '500 Internal Server Error — 처리되지 않은 RuntimeError', devtools: 'Terminal', chapterLink: '03' },
    { category: 'http', method: 'GET', path: '/errors/http/502', description: '502 Bad Gateway — 업스트림 서버 실패', devtools: 'Network', chapterLink: '01' },
    { category: 'http', method: 'GET', path: '/errors/http/503', description: '503 Service Unavailable — 서비스 불가 (Retry-After 헤더)', devtools: 'Network', chapterLink: '01' },

    // === 유효성 검사 (9) ===
    { category: 'validation', method: 'POST', path: '/errors/validation/missing-field', description: '필수 필드 누락 — detail[].loc 읽기', devtools: 'Network', chapterLink: '03', body: {} },
    { category: 'validation', method: 'POST', path: '/errors/validation/wrong-type', description: '타입 불일치 — "twenty" → int 변환 실패', devtools: 'Network', chapterLink: '03', body: { name: 'Alice', age: 'twenty', email: 'alice@test.com' } },
    { category: 'validation', method: 'POST', path: '/errors/validation/string-constraints', description: '문자열 제약 — min_length, pattern', devtools: 'Network', chapterLink: '03', body: { username: 'ab', bio: '' } },
    { category: 'validation', method: 'POST', path: '/errors/validation/number-range', description: '숫자 범위 — ge, le, gt', devtools: 'Network', chapterLink: '03', body: { age: -5, score: 150 } },
    { category: 'validation', method: 'POST', path: '/errors/validation/nested-model', description: '중첩 모델 — 깊은 loc 경로', devtools: 'Network', chapterLink: '03', body: { user: { name: 'Alice', address: { city: '' } } } },
    { category: 'validation', method: 'POST', path: '/errors/validation/email-format', description: '이메일 형식 — regex 유효성 검사', devtools: 'Network', chapterLink: '03', body: { email: 'not-an-email' } },
    { category: 'validation', method: 'POST', path: '/errors/validation/list-items', description: '빈 리스트 — 리스트 유효성 검사', devtools: 'Network', chapterLink: '03', body: { tags: [] } },
    { category: 'validation', method: 'GET', path: '/errors/validation/query-params?page=-1&size=0', description: '쿼리 파라미터 — Query도 검증됨', devtools: 'Network', chapterLink: '03' },
    { category: 'validation', method: 'GET', path: '/errors/validation/path-params/abc', description: '경로 파라미터 — Path 파라미터 검증', devtools: 'Network', chapterLink: '03' },

    // === DB 시뮬레이션 (10) ===
    { category: 'database', method: 'GET', path: '/errors/database/connection-refused', description: 'ConnectionRefusedError — DB 서버 꺼짐', devtools: 'Terminal', chapterLink: '04' },
    { category: 'database', method: 'GET', path: '/errors/database/connection-timeout', description: 'TimeoutError — DB 응답 지연', devtools: 'Terminal', chapterLink: '04' },
    { category: 'database', method: 'GET', path: '/errors/database/invalid-url', description: 'DATABASE_URL 파싱 실패 — 환경변수 누락', devtools: 'Terminal', chapterLink: '04' },
    { category: 'database', method: 'GET', path: '/errors/database/table-not-found', description: '테이블 없음 — 마이그레이션 미실행', devtools: 'Terminal', chapterLink: '04' },
    { category: 'database', method: 'GET', path: '/errors/database/column-not-found', description: '컬럼 없음 — 컬럼명 오타', devtools: 'Terminal', chapterLink: '04' },
    { category: 'database', method: 'POST', path: '/errors/database/integrity-unique', description: 'UNIQUE 위반 — 중복 데이터', devtools: 'Terminal', chapterLink: '04', body: { email: 'duplicate@test.com' } },
    { category: 'database', method: 'POST', path: '/errors/database/integrity-not-null', description: 'NOT NULL 위반 — 필수값 누락', devtools: 'Terminal', chapterLink: '04', body: {} },
    { category: 'database', method: 'POST', path: '/errors/database/type-mismatch', description: '타입 불일치 — DB 타입 오류', devtools: 'Terminal', chapterLink: '04', body: { age: 'not-a-number' } },
    { category: 'database', method: 'GET', path: '/errors/database/pool-exhausted', description: '풀 고갈 — 커넥션 풀', devtools: 'Terminal', chapterLink: '04' },
    { category: 'database', method: 'GET', path: '/errors/database/connection-leak', description: '연결 누수 — 연결 미반환', devtools: 'Terminal', chapterLink: '04' },

    // === 인증/인가 (6) ===
    { category: 'auth', method: 'POST', path: '/errors/auth/login', description: '로그인 (토큰 발급) — 셋업 단계', devtools: 'Network', chapterLink: '01', body: { username: 'admin', password: 'admin123' } },
    { category: 'auth', method: 'GET', path: '/errors/auth/protected', description: '보호된 엔드포인트 — Authorization 헤더 필요', devtools: 'Network', chapterLink: '01', requiresAuth: true },
    { category: 'auth', method: 'GET', path: '/errors/auth/invalid-token', description: '잘못된 토큰 — 토큰 형식/값 오류', devtools: 'Network', chapterLink: '01' },
    { category: 'auth', method: 'GET', path: '/errors/auth/expired-token', description: '만료된 토큰 — 토큰 만료 개념', devtools: 'Network', chapterLink: '01' },
    { category: 'auth', method: 'GET', path: '/errors/auth/admin-only', description: '관리자 전용 — 401 vs 403 차이', devtools: 'Network', chapterLink: '01', requiresAuth: true },
    { category: 'auth', method: 'POST', path: '/errors/auth/wrong-password', description: '비밀번호 틀림 — 로그인 실패 처리', devtools: 'Network', chapterLink: '01', body: { username: 'admin', password: 'wrong' } },

    // === 비즈니스 로직 (10) ===
    { category: 'logic', method: 'GET', path: '/errors/logic/division-by-zero?divisor=0', description: 'ZeroDivisionError — 0으로 나누기', devtools: 'Terminal', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/key-error', description: 'KeyError — 존재하지 않는 dict 키', devtools: 'Terminal', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/index-error', description: 'IndexError — 리스트 범위 초과', devtools: 'Terminal', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/type-error', description: 'TypeError — "hello" + 42', devtools: 'Terminal', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/attribute-error', description: 'AttributeError — 존재하지 않는 속성', devtools: 'Terminal', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/none-reference', description: 'NoneType 에러 — None.method() 패턴', devtools: 'Terminal', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/recursion-limit', description: 'RecursionError — 무한 재귀 (안전 제한)', devtools: 'Terminal', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/timeout?seconds=3', description: '느린 응답 — 최대 60초 지연', devtools: 'Network', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/value-error', description: 'ValueError — int("abc")', devtools: 'Terminal', chapterLink: '03' },
    { category: 'logic', method: 'GET', path: '/errors/logic/unhandled-vs-handled?handled=false', description: '처리/미처리 비교 — handled=true/false', devtools: 'Terminal', chapterLink: '03' },

    // === CORS (6) ===
    { category: 'cors', method: 'GET', path: '/errors/cors/no-headers', description: 'CORS 헤더 없음 — 브라우저 차단', devtools: 'Console', chapterLink: '05' },
    { category: 'cors', method: 'GET', path: '/errors/cors/wrong-origin', description: '잘못된 Origin — Origin 불일치', devtools: 'Console', chapterLink: '05' },
    { category: 'cors', method: 'GET', path: '/errors/cors/no-methods', description: '메서드 제한 — Method 불일치', devtools: 'Console', chapterLink: '05' },
    { category: 'cors', method: 'GET', path: '/errors/cors/preflight-fail', description: 'Preflight 실패 — OPTIONS 요청', devtools: 'Console', chapterLink: '05' },
    { category: 'cors', method: 'GET', path: '/errors/cors/correct', description: '정상 CORS — 올바른 설정 비교', devtools: 'Network', chapterLink: '05' },
    { category: 'cors', method: 'GET', path: '/errors/cors/test-page', description: 'CORS 테스트 페이지 — 브라우저에서 직접 테스트', devtools: 'Console', chapterLink: '05' },

    // === 요청/응답 (9) ===
    { category: 'request', method: 'POST', path: '/errors/request/wrong-content-type', description: '415 — Content-Type 헤더 오류', devtools: 'Network', chapterLink: '05', body: { data: 'test' }, contentType: 'text/plain' },
    { category: 'request', method: 'POST', path: '/errors/request/large-payload', description: '413 — 요청 크기 제한 (1KB)', devtools: 'Network', chapterLink: '05', body: { data: 'x'.repeat(2000) } },
    { category: 'request', method: 'POST', path: '/errors/request/malformed-json', description: 'JSON 파싱 실패 — 잘못된 JSON', devtools: 'Network', chapterLink: '05', rawBody: '{invalid json}' },
    { category: 'request', method: 'GET', path: '/errors/request/missing-header', description: '헤더 누락 — X-API-Key 필수', devtools: 'Network', chapterLink: '05' },
    { category: 'request', method: 'POST', path: '/errors/request/wrong-method', description: '405 — HTTP 메서드 불일치', devtools: 'Network', chapterLink: '05', body: {} },
    { category: 'request', method: 'GET', path: '/errors/request/html-instead-of-json', description: 'HTML 반환 — 응답 형식 불일치', devtools: 'Network', chapterLink: '05' },
    { category: 'request', method: 'GET', path: '/errors/request/empty-response', description: '204 — 빈 응답 처리', devtools: 'Network', chapterLink: '05' },
    { category: 'request', method: 'GET', path: '/errors/request/slow-response?delay=3', description: '느린 응답 — delay=N초', devtools: 'Network', chapterLink: '05' },
    { category: 'request', method: 'GET', path: '/errors/request/field-name-mismatch', description: 'snake_case — Python vs JS 네이밍', devtools: 'Network', chapterLink: '05' },

    // === 비동기 (5) ===
    { category: 'async', method: 'GET', path: '/errors/async/timeout', description: 'asyncio.TimeoutError — wait_for 타임아웃', devtools: 'Terminal', chapterLink: '03' },
    { category: 'async', method: 'GET', path: '/errors/async/blocking-call', description: '이벤트 루프 블로킹 — time.sleep vs asyncio.sleep', devtools: 'Terminal', chapterLink: '03' },
    { category: 'async', method: 'POST', path: '/errors/async/concurrent-counter?use_lock=false', description: 'Race Condition — use_lock=true/false', devtools: 'Network', chapterLink: '03', body: {} },
    { category: 'async', method: 'GET', path: '/errors/async/gather-partial-failure', description: '부분 실패 — gather(return_exceptions=True)', devtools: 'Terminal', chapterLink: '03' },
    { category: 'async', method: 'GET', path: '/errors/async/cancelled', description: 'CancelledError — 태스크 취소', devtools: 'Terminal', chapterLink: '03' },

    // === 파일/리소스 (5) ===
    { category: 'file', method: 'GET', path: '/errors/file/not-found?filename=missing.txt', description: 'FileNotFoundError — 파일 없음', devtools: 'Network', chapterLink: '03' },
    { category: 'file', method: 'GET', path: '/errors/file/permission-denied', description: 'PermissionError — 파일 권한', devtools: 'Terminal', chapterLink: '03' },
    { category: 'file', method: 'GET', path: '/errors/file/is-directory', description: 'IsADirectoryError — 디렉토리를 파일로 읽기', devtools: 'Terminal', chapterLink: '03' },
    { category: 'file', method: 'GET', path: '/errors/file/encoding-error', description: 'UnicodeDecodeError — 인코딩 오류', devtools: 'Terminal', chapterLink: '03' },
    { category: 'file', method: 'GET', path: '/errors/file/path-traversal?filename=../../etc/passwd', description: '403 경로 순회 차단 — 보안: ../ 공격', devtools: 'Network', chapterLink: '03' },
  ],

  DEVTOOLS_HINTS: {
    'Console': '🔍 브라우저 Console 탭에서 확인하세요. F12 → Console',
    'Network': '🔍 브라우저 Network 탭에서 확인하세요. F12 → Network → 해당 요청 클릭',
    'Terminal': '🔍 서버를 실행한 터미널에서 Traceback을 확인하세요.',
  },

  CHAPTER_MAP: {
    '01': { title: '에러는 어디에서 나는가', file: '01-에러는-어디에서-나는가.md' },
    '02': { title: '프론트엔드 에러', file: '02-프론트엔드-에러.md' },
    '03': { title: '백엔드 에러', file: '03-백엔드-에러.md' },
    '04': { title: '서버/DB 에러', file: '04-서버-DB-에러.md' },
    '05': { title: '프론트-백 통신 에러', file: '05-프론트-백-통신-에러.md' },
    '06': { title: '배포 에러', file: '06-배포-에러.md' },
    '07': { title: '디버깅 프로세스', file: '07-디버깅-프로세스.md' },
    '08': { title: '정적파일 서빙', file: '08-정적파일-서빙.md' },
    '09': { title: 'Git 에러', file: '09-Git-에러.md' },
    '10': { title: '라이브 데모', file: '10-라이브-데모.md' },
  },

  getEndpointsByCategory(categoryId) {
    return this.ENDPOINTS.filter(ep => ep.category === categoryId);
  },

  getCategoryById(categoryId) {
    return this.CATEGORIES.find(cat => cat.id === categoryId);
  }
};

window.APP_CONFIG = APP_CONFIG;
