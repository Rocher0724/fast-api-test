"""DB 에러 시뮬레이션 엔드포인트 — 강의 4장 연결.

실제 DB 없이 에러 메시지를 시뮬레이션합니다.
에러 메시지는 SQLAlchemy/psycopg2의 실제 메시지를 모방합니다.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/errors/database", tags=["3. DB 에러 시뮬레이션"])

# ── 인메모리 상태 ──────────────────────────────────────────────
_connection_leak_counter = 0
_MAX_POOL_SIZE = 5


# ── 모델 ───────────────────────────────────────────────────────
class InsertPayload(BaseModel):
    username: str
    email: str


class TypeMismatchPayload(BaseModel):
    id: str
    value: str


# ── 엔드포인트 ─────────────────────────────────────────────────
@router.get("/connection-refused", summary="DB 연결 거부 (4.1)")
def connection_refused():
    raise HTTPException(
        status_code=503,
        detail={
            "error": "ConnectionRefusedError",
            "message": "could not connect to server: Connection refused\n\tIs the server running on host \"localhost\" (127.0.0.1) and accepting TCP/IP connections on port 5432?",
            "lesson": "DB 서버가 꺼져 있거나 포트가 잘못되었을 때 발생합니다. DB 서버 상태와 포트 번호를 확인하세요.",
            "checklist": [
                "DB 서버가 실행 중인지 확인",
                "호스트와 포트가 올바른지 확인",
                "방화벽 설정 확인",
            ],
        },
    )


@router.get("/connection-timeout", summary="DB 연결 타임아웃 (4.1)")
def connection_timeout():
    raise HTTPException(
        status_code=504,
        detail={
            "error": "TimeoutError",
            "message": "connection to server at \"db.example.com\" (93.184.216.34), port 5432 failed: timeout expired",
            "lesson": "DB 서버가 응답하지 않거나 네트워크 문제가 있을 때 발생합니다. 네트워크 연결과 DB 서버 부하를 확인하세요.",
            "checklist": [
                "네트워크 연결 상태 확인",
                "DB 서버 부하 확인",
                "연결 타임아웃 설정 조정",
            ],
        },
    )


@router.get("/invalid-url", summary="DATABASE_URL 파싱 실패 (4.5)")
def invalid_url():
    raise HTTPException(
        status_code=500,
        detail={
            "error": "ArgumentError",
            "message": "Could not parse SQLAlchemy URL from string 'not-a-valid-url'",
            "lesson": "DATABASE_URL 환경변수가 없거나 형식이 잘못되었을 때 발생합니다. postgresql://user:pass@host:port/dbname 형식을 확인하세요.",
            "example_url": "postgresql://username:password@localhost:5432/mydb",
            "checklist": [
                ".env 파일에 DATABASE_URL이 설정되어 있는지 확인",
                "URL 형식이 올바른지 확인",
                "Render에서는 Internal Database URL 사용",
            ],
        },
    )


@router.get("/table-not-found", summary="테이블 없음 에러 (4.2)")
def table_not_found():
    raise HTTPException(
        status_code=500,
        detail={
            "error": "ProgrammingError",
            "message": '(psycopg2.errors.UndefinedTable) relation "users" does not exist\nLINE 1: SELECT * FROM users\n                      ^',
            "lesson": "테이블이 존재하지 않을 때 발생합니다. 마이그레이션을 실행했는지 확인하세요.",
            "checklist": [
                "alembic upgrade head 실행 여부 확인",
                "테이블 이름 대소문자 확인 (PostgreSQL은 소문자 기본)",
                "올바른 데이터베이스에 연결했는지 확인",
            ],
        },
    )


@router.get("/column-not-found", summary="컬럼 없음 에러 (4.2)")
def column_not_found():
    raise HTTPException(
        status_code=500,
        detail={
            "error": "ProgrammingError",
            "message": '(psycopg2.errors.UndefinedColumn) column "user_name" does not exist\nLINE 1: SELECT user_name FROM users\n                ^',
            "lesson": "컬럼명이 잘못되었을 때 발생합니다. 모델 필드명과 실제 DB 컬럼명이 일치하는지 확인하세요.",
            "hint": "혹시 'username'을 'user_name'으로 잘못 쓴 건 아닌가요?",
        },
    )


@router.post("/integrity-unique", summary="UNIQUE 제약 위반 (4.2)")
def integrity_unique(payload: InsertPayload):
    raise HTTPException(
        status_code=409,
        detail={
            "error": "IntegrityError",
            "message": f'(psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "users_email_key"\nDETAIL:  Key (email)=({payload.email}) already exists.',
            "lesson": "이미 존재하는 고유값을 삽입하려 할 때 발생합니다. INSERT 전에 중복 확인을 하거나 UPSERT를 사용하세요.",
        },
    )


@router.post("/integrity-not-null", summary="NOT NULL 위반 (4.2)")
def integrity_not_null(payload: InsertPayload):
    raise HTTPException(
        status_code=400,
        detail={
            "error": "IntegrityError",
            "message": '(psycopg2.errors.NotNullViolation) null value in column "email" of relation "users" violates not-null constraint\nDETAIL:  Failing row contains (1, testuser, null).',
            "lesson": "NOT NULL 제약이 있는 컬럼에 NULL을 넣으려 할 때 발생합니다. 필수 필드가 빠지지 않았는지 확인하세요.",
        },
    )


@router.post("/type-mismatch", summary="DB 타입 불일치 (4.2)")
def type_mismatch(payload: TypeMismatchPayload):
    raise HTTPException(
        status_code=400,
        detail={
            "error": "DataError",
            "message": f'(psycopg2.errors.InvalidTextRepresentation) invalid input syntax for type integer: "{payload.id}"',
            "lesson": "DB 컬럼 타입과 맞지 않는 값을 넣으려 할 때 발생합니다. 데이터 타입을 확인하세요.",
        },
    )


@router.get("/pool-exhausted", summary="커넥션 풀 고갈 (4.3)")
def pool_exhausted():
    raise HTTPException(
        status_code=503,
        detail={
            "error": "TimeoutError",
            "message": "QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30.00",
            "lesson": "커넥션 풀의 모든 연결이 사용 중일 때 발생합니다. 연결을 제때 반환하지 않으면 풀이 고갈됩니다.",
            "solutions": [
                "DB 세션을 try/finally로 확실히 닫기",
                "풀 크기 늘리기 (pool_size, max_overflow)",
                "쿼리 최적화로 연결 점유 시간 줄이기",
            ],
        },
    )


@router.get("/connection-leak", summary="연결 누수 시뮬레이션 (4.3)")
def connection_leak():
    global _connection_leak_counter
    _connection_leak_counter += 1

    status = {
        "active_connections": _connection_leak_counter,
        "max_pool_size": _MAX_POOL_SIZE,
        "leaked": _connection_leak_counter > _MAX_POOL_SIZE,
    }

    if _connection_leak_counter > _MAX_POOL_SIZE:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "ConnectionLeakDetected",
                "message": f"활성 연결 수({_connection_leak_counter})가 풀 크기({_MAX_POOL_SIZE})를 초과했습니다!",
                "lesson": "DB 연결을 사용 후 반환하지 않으면 누수가 발생합니다. FastAPI에서는 Depends()로 세션 생명주기를 관리하세요.",
                "hint": "서버를 재시작하면 카운터가 초기화됩니다.",
                **status,
            },
        )

    return {
        "message": f"연결 획득 ({_connection_leak_counter}/{_MAX_POOL_SIZE})",
        **status,
        "lesson": "이 엔드포인트를 반복 호출하면 연결 누수를 시뮬레이션합니다. 연결이 반환되지 않는 상황을 체험하세요.",
    }
