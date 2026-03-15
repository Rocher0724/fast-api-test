# 에러 학습 API 가이드

FastAPI 디버깅 강의 실습용 API입니다. `/docs`(Swagger UI)에서 직접 테스트하며 학습할 수 있습니다.

## 시작하기

```bash
cd /Users/rocher/Documents/intea/fast-api-test
python -m uvicorn app.main:app --reload
```

브라우저에서 `http://localhost:8000/docs` 열기

---

## 1. HTTP 상태 코드 에러 (`/errors/http`) — 12개

> 강의 1.3장 HTTP 상태 코드와 연결

| Route | Method | 에러 코드 | 학습 포인트 |
|-------|--------|----------|------------|
| `/errors/http/400` | GET | 400 | 클라이언트 요청 오류 |
| `/errors/http/401` | GET | 401 | 인증 필요 (WWW-Authenticate 헤더 확인) |
| `/errors/http/403` | GET | 403 | 인증됐지만 권한 없음 |
| `/errors/http/404` | GET | 404 | 리소스 없음 |
| `/errors/http/405` | POST | 405 | GET으로 호출하면 405 발생 |
| `/errors/http/408` | GET | 408 | 요청 타임아웃 |
| `/errors/http/409` | POST | 409 | 중복 리소스 (username 충돌) |
| `/errors/http/422` | POST | 422 | Pydantic 자동 유효성 검사 |
| `/errors/http/429` | GET | 429 | Rate Limiting (3회 초과 시 차단) |
| `/errors/http/500` | GET | 500 | 처리되지 않은 RuntimeError |
| `/errors/http/502` | GET | 502 | 업스트림 서버 실패 |
| `/errors/http/503` | GET | 503 | 서비스 불가 (Retry-After 헤더) |

### 테스트 방법
- `/docs`에서 각 엔드포인트를 "Try it out"으로 실행
- 응답의 HTTP 상태 코드와 에러 메시지를 확인
- `/errors/http/429`는 3번 호출 후 4번째부터 차단 (서버 재시작으로 리셋)

---

## 2. 유효성 검사 에러 (`/errors/validation`) — 9개

> 강의 3.2장 422 에러와 연결

| Route | Method | 에러 | 학습 포인트 |
|-------|--------|------|------------|
| `/errors/validation/missing-field` | POST | 필수 필드 누락 | `detail[].loc` 읽기 |
| `/errors/validation/wrong-type` | POST | 타입 불일치 | `"twenty"` → int 변환 실패 |
| `/errors/validation/string-constraints` | POST | 문자열 제약 | `min_length`, `pattern` |
| `/errors/validation/number-range` | POST | 숫자 범위 | `ge`, `le`, `gt` |
| `/errors/validation/nested-model` | POST | 중첩 모델 | 깊은 `loc` 경로 |
| `/errors/validation/email-format` | POST | 이메일 형식 | regex 유효성 검사 |
| `/errors/validation/list-items` | POST | 빈 리스트 | 리스트 유효성 검사 |
| `/errors/validation/query-params` | GET | 쿼리 파라미터 | Body가 아닌 Query도 검증 |
| `/errors/validation/path-params/{id}` | GET | 경로 파라미터 | Path 파라미터 검증 |

### 테스트 방법
- POST 엔드포인트에서 JSON body의 필드를 일부러 빼거나 잘못된 타입으로 전송
- 422 응답의 `detail` 배열에서 `loc`, `msg`, `type` 필드를 읽는 연습
- 예: `{"name": "Alice", "age": "twenty", "email": "not-email"}` → 어떤 에러가 나오는지 확인

---

## 3. DB 에러 시뮬레이션 (`/errors/database`) — 10개

> 강의 4장과 연결. 실제 DB 없이 에러 메시지 시뮬레이션

| Route | Method | 에러 | 학습 포인트 |
|-------|--------|------|------------|
| `/errors/database/connection-refused` | GET | ConnectionRefusedError | DB 서버 꺼짐 (4.1) |
| `/errors/database/connection-timeout` | GET | TimeoutError | DB 응답 지연 (4.1) |
| `/errors/database/invalid-url` | GET | DATABASE_URL 파싱 실패 | 환경변수 누락 (4.5) |
| `/errors/database/table-not-found` | GET | 테이블 없음 | 마이그레이션 미실행 (4.2) |
| `/errors/database/column-not-found` | GET | 컬럼 없음 | 컬럼명 오타 (4.2) |
| `/errors/database/integrity-unique` | POST | UNIQUE 위반 | 중복 데이터 (4.2) |
| `/errors/database/integrity-not-null` | POST | NOT NULL 위반 | 필수값 누락 (4.2) |
| `/errors/database/type-mismatch` | POST | 타입 불일치 | DB 타입 오류 (4.2) |
| `/errors/database/pool-exhausted` | GET | 풀 고갈 | 커넥션 풀 (4.3) |
| `/errors/database/connection-leak` | GET | 연결 누수 | 연결 미반환 (4.3) |

### 테스트 방법
- GET 엔드포인트를 호출하면 실제 PostgreSQL/SQLAlchemy 에러 메시지가 재현됨
- `/errors/database/connection-leak`를 반복 호출하면 풀 크기(5) 초과 시 에러 발생
- 각 에러의 `checklist`를 통해 실제 상황에서의 해결 방법 학습

---

## 4. 인증/인가 에러 (`/errors/auth`) — 6개

> 401 vs 403 구분 학습

| Route | Method | 설명 | 학습 포인트 |
|-------|--------|------|------------|
| `/errors/auth/login` | POST | 로그인 (토큰 발급) | 셋업 단계 |
| `/errors/auth/protected` | GET | 보호된 엔드포인트 | Authorization 헤더 필요 |
| `/errors/auth/invalid-token` | GET | 잘못된 토큰 | 토큰 형식/값 오류 |
| `/errors/auth/expired-token` | GET | 만료된 토큰 | 토큰 만료 개념 |
| `/errors/auth/admin-only` | GET | 관리자 전용 | 401 vs 403 차이 |
| `/errors/auth/wrong-password` | POST | 비밀번호 틀림 | 로그인 실패 처리 |

### 테스트 순서
1. `/errors/auth/login`에서 `{"username": "admin", "password": "admin123"}` 또는 `{"username": "user", "password": "user123"}`로 토큰 발급
2. 발급받은 토큰을 복사
3. `/errors/auth/protected`에서 Authorization 헤더에 `Bearer <토큰>` 입력
4. `/errors/auth/admin-only`에서 user 토큰 vs admin 토큰의 차이 확인
5. 잘못된 토큰이나 헤더 없이 호출하여 401 에러 확인

---

## 5. 비즈니스 로직 에러 (`/errors/logic`) — 10개

> 강의 3.2장 500 에러, 부록 A 에러 사전과 연결

| Route | Method | 에러 | 학습 포인트 |
|-------|--------|------|------------|
| `/errors/logic/division-by-zero` | GET | ZeroDivisionError | `?divisor=0` |
| `/errors/logic/key-error` | GET | KeyError | 존재하지 않는 dict 키 |
| `/errors/logic/index-error` | GET | IndexError | 리스트 범위 초과 |
| `/errors/logic/type-error` | GET | TypeError | `"hello" + 42` |
| `/errors/logic/attribute-error` | GET | AttributeError | 존재하지 않는 속성 |
| `/errors/logic/none-reference` | GET | NoneType 에러 | `None.method()` 패턴 |
| `/errors/logic/recursion-limit` | GET | RecursionError | 무한 재귀 (안전 제한) |
| `/errors/logic/timeout` | GET | 느린 응답 | `?seconds=10` (최대 60초) |
| `/errors/logic/value-error` | GET | ValueError | `int("abc")` |
| `/errors/logic/unhandled-vs-handled` | GET | 처리/미처리 비교 | `?handled=true/false` |

### 테스트 방법
- 각 엔드포인트 호출 시 500 Internal Server Error 발생 확인
- `/errors/logic/unhandled-vs-handled`에서 `?handled=true` vs `?handled=false` 비교
- 서버 로그(터미널)에서 Traceback 확인 연습

---

## 6. CORS 에러 (`/errors/cors`) — 6개

> 강의 5.1장과 연결

| Route | Method | 설명 | 학습 포인트 |
|-------|--------|------|------------|
| `/errors/cors/no-headers` | GET | CORS 헤더 없음 | 브라우저 차단 |
| `/errors/cors/wrong-origin` | GET | 잘못된 Origin | Origin 불일치 |
| `/errors/cors/no-methods` | GET | 메서드 제한 | Method 불일치 |
| `/errors/cors/preflight-fail` | OPTIONS/GET | Preflight 실패 | OPTIONS 요청 |
| `/errors/cors/correct` | GET | 정상 CORS | 올바른 설정 비교 |
| `/errors/cors/test-page` | GET | 테스트 페이지 | 브라우저에서 직접 테스트 |

### 테스트 방법
1. 브라우저에서 `http://localhost:8000/errors/cors/test-page` 열기
2. 각 버튼을 클릭하여 CORS 동작 확인
3. DevTools Console과 Network 탭에서 실제 CORS 에러 메시지 확인
4. "올바른 CORS"와 다른 응답의 헤더 차이 비교

---

## 7. 요청/응답 에러 (`/errors/request`) — 9개

> 강의 5.2~5.3장과 연결

| Route | Method | 에러 | 학습 포인트 |
|-------|--------|------|------------|
| `/errors/request/wrong-content-type` | POST | 415 | Content-Type 헤더 |
| `/errors/request/large-payload` | POST | 413 | 요청 크기 제한 (1KB) |
| `/errors/request/malformed-json` | POST | JSON 파싱 실패 | 잘못된 JSON |
| `/errors/request/missing-header` | GET | 헤더 누락 | X-API-Key 필수 |
| `/errors/request/wrong-method` | POST | 405 | HTTP 메서드 불일치 |
| `/errors/request/html-instead-of-json` | GET | HTML 반환 | 응답 형식 불일치 |
| `/errors/request/empty-response` | GET | 204 | 빈 응답 처리 |
| `/errors/request/slow-response` | GET | 느린 응답 | `?delay=5` |
| `/errors/request/field-name-mismatch` | GET | snake_case | Python vs JS 네이밍 |

---

## 8. 비동기 에러 (`/errors/async`) — 5개

| Route | Method | 에러 | 학습 포인트 |
|-------|--------|------|------------|
| `/errors/async/timeout` | GET | asyncio.TimeoutError | `wait_for` 타임아웃 |
| `/errors/async/blocking-call` | GET | 이벤트 루프 블로킹 | `time.sleep` vs `asyncio.sleep` |
| `/errors/async/concurrent-counter` | POST | Race Condition | `?use_lock=true/false` |
| `/errors/async/gather-partial-failure` | GET | 부분 실패 | `gather(return_exceptions=True)` |
| `/errors/async/cancelled` | GET | CancelledError | 태스크 취소 |

---

## 9. 파일/리소스 에러 (`/errors/file`) — 5개

| Route | Method | 에러 | 학습 포인트 |
|-------|--------|------|------------|
| `/errors/file/not-found` | GET | FileNotFoundError | `?filename=xxx` |
| `/errors/file/permission-denied` | GET | PermissionError | 파일 권한 |
| `/errors/file/is-directory` | GET | IsADirectoryError | 디렉토리를 파일로 읽기 |
| `/errors/file/encoding-error` | GET | UnicodeDecodeError | 인코딩 오류 |
| `/errors/file/path-traversal` | GET | 403 경로 순회 차단 | 보안: `../` 공격 |

---

## 강의 챕터 매핑

| 강의 챕터 | API 카테고리 |
|----------|-------------|
| 1장 - 에러는 어디에서 나는가 | `/errors/http` (전체 상태 코드 개요) |
| 3장 - 백엔드 에러 | `/errors/validation`, `/errors/logic` |
| 4장 - 서버/DB 에러 | `/errors/database` |
| 5장 - 프론트-백 통신 에러 | `/errors/cors`, `/errors/request` |

---

## 참고

- 모든 인메모리 상태(카운터, 토큰)는 서버 재시작 시 초기화됩니다
- DB 에러는 실제 DB 없이 에러 메시지만 시뮬레이션합니다
- 타임아웃 관련 엔드포인트는 최대 60초로 안전하게 제한됩니다
- CORS 테스트는 브라우저에서 직접 실행해야 의미 있습니다 (Swagger UI는 Same-Origin)
