"""HTTP 상태 코드 에러 엔드포인트 — 강의 1.3장 연결."""

import time
from collections import defaultdict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/errors/http", tags=["1. HTTP 상태 코드 에러"])

# ── 인메모리 상태 ──────────────────────────────────────────────
_rate_limit_counter: dict[str, int] = defaultdict(int)


# ── 모델 ───────────────────────────────────────────────────────
class ConflictPayload(BaseModel):
    username: str


class UnprocessablePayload(BaseModel):
    name: str
    age: int
    email: str


# ── 엔드포인트 ─────────────────────────────────────────────────
@router.get("/400", summary="400 Bad Request")
def bad_request():
    raise HTTPException(
        status_code=400,
        detail={
            "error": "Bad Request",
            "message": "클라이언트 요청이 잘못되었습니다.",
            "lesson": "400은 서버가 요청을 이해할 수 없을 때 반환됩니다. 요청 파라미터나 형식을 확인하세요.",
        },
    )


@router.get("/401", summary="401 Unauthorized")
def unauthorized():
    raise HTTPException(
        status_code=401,
        detail={
            "error": "Unauthorized",
            "message": "인증이 필요합니다.",
            "lesson": "401은 인증(로그인)이 필요하다는 의미입니다. WWW-Authenticate 헤더를 확인하세요.",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/403", summary="403 Forbidden")
def forbidden():
    raise HTTPException(
        status_code=403,
        detail={
            "error": "Forbidden",
            "message": "이 리소스에 접근할 권한이 없습니다.",
            "lesson": "403은 인증은 되었지만 권한이 부족할 때 반환됩니다. 401과의 차이를 이해하세요.",
        },
    )


@router.get("/404", summary="404 Not Found")
def not_found():
    raise HTTPException(
        status_code=404,
        detail={
            "error": "Not Found",
            "message": "요청한 리소스를 찾을 수 없습니다.",
            "lesson": "404는 URL 경로가 잘못되었거나 리소스가 삭제되었을 때 발생합니다.",
        },
    )


@router.post("/405", summary="405 Method Not Allowed (POST만 허용)")
def method_not_allowed():
    """이 엔드포인트는 POST만 허용합니다. GET으로 호출하면 FastAPI가 자동으로 405를 반환합니다."""
    return {
        "message": "POST 요청 성공!",
        "lesson": "이 엔드포인트를 GET으로 호출하면 405 Method Not Allowed가 발생합니다.",
    }


@router.get("/408", summary="408 Request Timeout")
def request_timeout():
    raise HTTPException(
        status_code=408,
        detail={
            "error": "Request Timeout",
            "message": "요청 처리 시간이 초과되었습니다.",
            "lesson": "408은 서버가 클라이언트의 요청을 기다리다 타임아웃된 경우입니다. 네트워크 상태를 확인하세요.",
        },
    )


@router.post("/409", summary="409 Conflict")
def conflict(payload: ConflictPayload):
    raise HTTPException(
        status_code=409,
        detail={
            "error": "Conflict",
            "message": f"'{payload.username}' 사용자명이 이미 존재합니다.",
            "lesson": "409는 리소스 충돌(예: 중복 사용자명)을 나타냅니다. 다른 값을 시도하거나 기존 리소스를 확인하세요.",
        },
    )


@router.post("/422", summary="422 Unprocessable Entity")
def unprocessable_entity(payload: UnprocessablePayload):
    """정상 요청을 보내면 성공합니다. 필드를 빼거나 잘못된 타입을 보내면 422가 발생합니다."""
    return {
        "message": "유효성 검사 통과!",
        "data": payload.model_dump(),
        "lesson": "Pydantic 모델에 맞지 않는 요청을 보내면 FastAPI가 자동으로 422를 반환합니다.",
    }


@router.get("/429", summary="429 Too Many Requests")
def too_many_requests():
    _rate_limit_counter["global"] += 1
    count = _rate_limit_counter["global"]

    if count > 3:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Too Many Requests",
                "message": f"요청 횟수 초과 ({count}회). 3회까지 허용됩니다.",
                "lesson": "429는 Rate Limiting에 걸렸을 때 발생합니다. Retry-After 헤더를 확인하고 잠시 후 다시 시도하세요.",
                "hint": "서버를 재시작하면 카운터가 초기화됩니다.",
            },
            headers={"Retry-After": "30"},
        )

    return {
        "message": f"요청 성공 ({count}/3)",
        "remaining": 3 - count,
        "lesson": "이 엔드포인트는 3회까지만 허용됩니다. 초과하면 429 에러가 발생합니다.",
    }


@router.get("/500", summary="500 Internal Server Error")
def internal_server_error():
    raise RuntimeError(
        "의도적인 서버 에러입니다. 프로덕션에서는 이런 에러가 로그에 기록되어야 합니다."
    )


@router.get("/502", summary="502 Bad Gateway")
def bad_gateway():
    raise HTTPException(
        status_code=502,
        detail={
            "error": "Bad Gateway",
            "message": "업스트림 서버로부터 잘못된 응답을 받았습니다.",
            "lesson": "502는 프록시/게이트웨이가 업스트림 서버로부터 유효하지 않은 응답을 받았을 때 발생합니다.",
        },
    )


@router.get("/503", summary="503 Service Unavailable")
def service_unavailable():
    raise HTTPException(
        status_code=503,
        detail={
            "error": "Service Unavailable",
            "message": "서버가 일시적으로 요청을 처리할 수 없습니다.",
            "lesson": "503은 서버 과부하나 유지보수 중일 때 발생합니다. Retry-After 헤더를 확인하세요.",
        },
        headers={"Retry-After": "60"},
    )
