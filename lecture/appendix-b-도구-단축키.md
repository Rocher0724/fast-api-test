# 부록 B. 유용한 도구 / 단축키 모음

---

## 브라우저 개발자 도구 (Chrome DevTools)

### 필수 단축키

| 동작 | Mac | Windows |
|------|-----|---------|
| DevTools 열기/닫기 | `Cmd + Option + I` | `F12` |
| Console 탭 바로 열기 | `Cmd + Option + J` | `Ctrl + Shift + J` |
| Elements 탭 (요소 검사) | `Cmd + Option + C` | `Ctrl + Shift + C` |
| 강력 새로고침 (캐시 무시) | `Cmd + Shift + R` | `Ctrl + Shift + R` |
| DevTools 내 검색 | `Cmd + F` | `Ctrl + F` |

### DevTools 탭별 용도

| 탭 | 언제 쓰는가 | 핵심 기능 |
|----|-----------|----------|
| **Console** | JS 에러 확인 | 빨간 에러 메시지, console.log 출력 |
| **Network** | API 통신 확인 | 요청/응답, 상태 코드, Payload |
| **Elements** | HTML/CSS 확인 | 실시간 스타일 수정, 구조 확인 |
| **Application** | 저장소 확인 | localStorage, 쿠키, 세션 |
| **Sources** | JS 디버깅 | 브레이크포인트, 단계별 실행 |

### Network 탭 유용한 기능

| 기능 | 설명 |
|------|------|
| **Filter (XHR)** | API 요청만 필터링 (XHR/Fetch 클릭) |
| **Preserve log** | 페이지 이동 시에도 기록 유지 |
| **Disable cache** | 캐시 비활성화 (DevTools 열린 동안) |
| **Throttling** | 느린 네트워크 시뮬레이션 |

---

## 터미널 (서버 관리)

### FastAPI / Uvicorn

| 명령어 | 설명 |
|--------|------|
| `uvicorn app.main:app --reload` | 서버 실행 (코드 변경 시 자동 재시작) |
| `uvicorn app.main:app --reload --port 8080` | 포트 변경하여 실행 |
| `Ctrl + C` | 서버 종료 |

### pip (패키지 관리)

| 명령어 | 설명 |
|--------|------|
| `pip install 패키지명` | 패키지 설치 |
| `pip install -r requirements.txt` | requirements.txt의 모든 패키지 설치 |
| `pip freeze` | 설치된 패키지 목록 출력 |
| `pip freeze > requirements.txt` | 설치된 패키지를 requirements.txt로 저장 |

### Git

| 명령어 | 설명 |
|--------|------|
| `git status` | 현재 상태 확인 (가장 많이 쓰는 명령어) |
| `git diff` | 변경 내용 확인 |
| `git add .` | 모든 변경 파일 스테이징 |
| `git commit -m "메시지"` | 커밋 생성 |
| `git push origin main` | GitHub에 올리기 |
| `git pull origin main` | GitHub에서 가져오기 |
| `git log --oneline` | 커밋 기록 간단히 보기 |
| `git checkout -- 파일명` | 수정한 파일 되돌리기 (커밋 전) |

---

## FastAPI 내장 도구

| 도구 | URL | 용도 |
|------|-----|------|
| **Swagger UI** | `http://localhost:8000/docs` | API 테스트 (가장 많이 사용) |
| **ReDoc** | `http://localhost:8000/redoc` | API 문서 (읽기 편한 형태) |
| **OpenAPI JSON** | `http://localhost:8000/openapi.json` | API 스펙 파일 |

---

## VS Code 유용한 단축키

| 동작 | Mac | Windows |
|------|-----|---------|
| 파일 빠른 열기 | `Cmd + P` | `Ctrl + P` |
| 전체 검색 | `Cmd + Shift + F` | `Ctrl + Shift + F` |
| 터미널 열기/닫기 | `` Ctrl + ` `` | `` Ctrl + ` `` |
| 현재 줄 이동 | `Option + ↑/↓` | `Alt + ↑/↓` |
| 줄 복제 | `Cmd + Shift + D` | `Ctrl + Shift + D` |
| 되돌리기 | `Cmd + Z` | `Ctrl + Z` |
| 저장 | `Cmd + S` | `Ctrl + S` |
| 멀티커서 | `Cmd + D` (같은 단어 선택) | `Ctrl + D` |

### VS Code 추천 확장

| 확장 | 용도 |
|------|------|
| **Python** | Python 문법 지원, 자동완성 |
| **Pylance** | Python 타입 체크, 빠른 분석 |
| **Live Server** | HTML 파일을 로컬 서버로 실시간 미리보기 |
| **REST Client** | VS Code 안에서 API 테스트 |
| **GitLens** | Git 히스토리를 코드 줄 단위로 확인 |

---

## 유용한 외부 도구

| 도구 | 용도 | URL |
|------|------|-----|
| **JSONFormatter** | JSON 응답을 보기 좋게 정리하는 Chrome 확장 | Chrome 웹 스토어 |
| **Postman** | API 테스트 도구 (GUI 환경) | postman.com |
| **DBeaver** | DB 직접 접속해서 데이터 확인 | dbeaver.io |
| **UptimeRobot** | 사이트 모니터링 (다운 알림) | uptimerobot.com |
