# 부록 A. 자주 보는 에러 메시지 사전

> 에러 메시지 → 원인 → 해결법 빠른 참조.
> Ctrl+F (또는 Cmd+F)로 에러 메시지를 검색하세요.

---

## 프론트엔드 (브라우저 Console)

| 에러 메시지 | 원인 | 해결법 |
|------------|------|--------|
| `Uncaught ReferenceError: xxx is not defined` | 변수명 오타 또는 미선언 | 변수명 확인, 선언 여부 확인 |
| `Uncaught TypeError: Cannot read properties of undefined (reading 'xxx')` | undefined 값에서 속성을 읽으려 함 | 해당 변수가 왜 undefined인지 확인, `console.log()`로 값 추적 |
| `Uncaught TypeError: xxx is not a function` | 함수가 아닌 것을 함수로 호출 | 변수명/함수명 확인, import 확인 |
| `Uncaught SyntaxError: Unexpected token` | JS 문법 오류 (괄호, 쉼표 등) | 해당 줄 근처의 괄호, 쉼표, 따옴표 확인 |
| `Uncaught SyntaxError: Unexpected end of input` | 괄호/중괄호가 안 닫힘 | 열고 닫는 괄호 쌍 확인 |
| `Access to fetch at 'xxx' has been blocked by CORS policy` | CORS 설정 누락 | FastAPI에 CORSMiddleware 추가 (5장) |
| `Failed to fetch` / `net::ERR_CONNECTION_REFUSED` | 서버가 안 돌고 있음 | 서버 실행 상태 확인 |
| `SyntaxError: JSON.parse: unexpected character` | JSON 형식이 아닌 응답을 파싱 시도 | 서버 응답이 JSON인지 확인 (HTML 에러 페이지가 올 수 있음) |

---

## 백엔드 (FastAPI / Python)

### HTTP 에러 응답

| 상태 코드 | 에러 메시지 | 원인 | 해결법 |
|----------|-----------|------|--------|
| **400** | `Bad Request` | 요청 형식이 잘못됨 | Request Body/Query 형식 확인 |
| **401** | `Not authenticated` | 인증 토큰 없음/만료 | 로그인 상태, 토큰 유효기간 확인 |
| **403** | `Forbidden` | 권한 없음 | 사용자 권한 설정 확인 |
| **404** | `Not Found` | URL 경로가 없음 | URL 오타 확인, 서버 라우트와 비교 |
| **405** | `Method Not Allowed` | HTTP 메서드 불일치 | GET/POST/PUT/DELETE 확인 |
| **422** | `Unprocessable Entity` | 데이터 검증 실패 | Response의 `detail`에서 어떤 필드가 잘못됐는지 확인 |
| **500** | `Internal Server Error` | 서버 코드 버그 | 서버 터미널 Traceback 확인 |
| **502** | `Bad Gateway` | 서버 프로세스가 죽음 | Render Logs에서 크래시 원인 확인 |
| **503** | `Service Unavailable` | 서버 과부하 또는 콜드 스타트 | 잠시 후 재시도, Render 무료 플랜이면 대기 |

### Python 에러

| 에러 메시지 | 원인 | 해결법 |
|------------|------|--------|
| `ModuleNotFoundError: No module named 'xxx'` | 패키지 미설치 | `pip install xxx` + requirements.txt 추가 |
| `ImportError: cannot import name 'xxx'` | import 경로 오류 | 클래스/함수명, 파일명 확인 |
| `NameError: name 'xxx' is not defined` | 변수/함수 미정의 | 오타 확인, 정의 순서 확인 |
| `TypeError: xxx() got an unexpected keyword argument` | 함수 파라미터명 오류 | 함수 정의와 호출부 파라미터명 비교 |
| `AttributeError: 'xxx' object has no attribute 'yyy'` | 객체에 없는 속성 접근 | 객체 타입 확인, 속성명 오타 확인 |
| `KeyError: 'xxx'` | 딕셔너리에 없는 키 접근 | `.get('xxx')` 사용, 키 존재 여부 확인 |
| `ValueError: invalid literal for int()` | 문자열→숫자 변환 실패 | 입력값이 정말 숫자인지 확인 |
| `IndentationError: unexpected indent` | 들여쓰기 오류 | 탭/스페이스 혼용 확인, 들여쓰기 맞추기 |

---

## 데이터베이스 (SQLAlchemy / PostgreSQL)

| 에러 메시지 | 원인 | 해결법 |
|------------|------|--------|
| `OperationalError: could not connect to server: Connection refused` | DB 서버 꺼짐 또는 주소 오류 | DATABASE_URL 확인, DB 서버 상태 확인 |
| `OperationalError: connection timed out` | DB 서버 응답 없음 | 네트워크, 방화벽 확인 |
| `ProgrammingError: relation "xxx" does not exist` | 테이블 없음 | 마이그레이션 실행 |
| `ProgrammingError: column "xxx" does not exist` | 컬럼 없음 | 마이그레이션 실행, 컬럼명 오타 확인 |
| `IntegrityError: duplicate key value violates unique constraint` | unique 값 중복 | 중복 체크 로직 추가 |
| `IntegrityError: null value in column "xxx" violates not-null constraint` | 필수 필드에 값 없음 | 해당 필드에 값 전달 확인 |
| `DataError: invalid input syntax for type integer: "xxx"` | 타입 불일치 | DB 컬럼 타입과 입력값 타입 확인 |
| `TimeoutError: QueuePool limit reached` | 커넥션 풀 부족 | 연결 반환(db.close) 확인, pool_size 조정 |

---

## 배포 (Render.com)

| 에러 / 상황 | 원인 | 해결법 |
|------------|------|--------|
| Deploy 실패: `No matching distribution found` | requirements.txt에 없는 패키지 | 패키지명/버전 확인 |
| Deploy 실패: `SyntaxError` | Python 버전 불일치 | runtime.txt로 버전 지정 |
| 서버 시작 후 바로 죽음 | Start Command 오류 또는 import 에러 | Render Logs에서 첫 에러 확인 |
| 사이트 접속 시 30초+ 대기 | 콜드 스타트 (무료 플랜) | 정상 동작, 에러 아님 |
| 갑자기 DB 연결 실패 | 무료 DB 90일 만료 | Render에서 DB 상태 확인, 재생성 |
| `FileNotFoundError: static/index.html` | 파일 경로 대소문자 또는 경로 오류 | 대소문자 확인, 절대 경로 사용 |

---

## Git

| 에러 메시지 | 원인 | 해결법 |
|------------|------|--------|
| `rejected: non-fast-forward` | 원격과 로컬 히스토리 불일치 | `git pull` 먼저 실행 |
| `CONFLICT (content): Merge conflict` | 같은 부분을 다르게 수정 | 파일 열어서 충돌 수동 해결 |
| `nothing to commit, working tree clean` | 변경사항 없거나 add 안 함 | `git status`로 확인 |
| `File xxx exceeds GitHub's file size limit` | 100MB 초과 파일 | .gitignore에 추가 |
| `Permission denied (publickey)` | SSH 키 미설정 | HTTPS URL로 변경하거나 SSH 키 등록 |
