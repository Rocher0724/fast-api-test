from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.routers import (
    async_errors,
    auth_errors,
    business_logic_errors,
    cors_errors,
    database_errors,
    file_errors,
    http_errors,
    lecture,
    request_response_errors,
    validation_errors,
)

app = FastAPI(
    title="에러 학습 API",
    description="FastAPI 디버깅 강의 실습용 API. 다양한 에러를 의도적으로 발생시켜 학습할 수 있습니다.",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(http_errors.router)
app.include_router(validation_errors.router)
app.include_router(database_errors.router)
app.include_router(auth_errors.router)
app.include_router(business_logic_errors.router)
app.include_router(cors_errors.router)
app.include_router(request_response_errors.router)
app.include_router(async_errors.router)
app.include_router(file_errors.router)
app.include_router(lecture.router)


@app.get("/api/info", tags=["Index"])
def api_info():
    return {
        "message": "에러 학습 API에 오신 것을 환영합니다!",
        "docs": "/docs 에서 Swagger UI를 확인하세요.",
        "categories": {
            "/errors/http": "1. HTTP 상태 코드 에러 (12개)",
            "/errors/validation": "2. 유효성 검사 에러 (9개)",
            "/errors/database": "3. DB 에러 시뮬레이션 (10개)",
            "/errors/auth": "4. 인증/인가 에러 (6개)",
            "/errors/logic": "5. 비즈니스 로직 에러 (10개)",
            "/errors/cors": "6. CORS 에러 (6개)",
            "/errors/request": "7. 요청/응답 에러 (9개)",
            "/errors/async": "8. 비동기 에러 (5개)",
            "/errors/file": "9. 파일/리소스 에러 (5개)",
        },
        "total_endpoints": 72,
    }


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/lecture", include_in_schema=False)
def lecture_page():
    return FileResponse(STATIC_DIR / "lecture.html")


@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return FileResponse(STATIC_DIR / "dashboard.html")


@app.get("/dataflow", include_in_schema=False)
def dataflow_page():
    return FileResponse(STATIC_DIR / "dataflow.html")


@app.get("/health", tags=["Index"])
def health_check():
    return {"status": "ok"}


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
