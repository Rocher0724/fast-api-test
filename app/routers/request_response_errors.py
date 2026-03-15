"""요청/응답 형식 에러 엔드포인트 — 강의 5.2~5.3장 연결."""

import asyncio

from fastapi import APIRouter, Header, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel

router = APIRouter(prefix="/errors/request", tags=["7. 요청/응답 에러"])


class GenericPayload(BaseModel):
    data: str


# ── 엔드포인트 ─────────────────────────────────────────────────
@router.post("/wrong-content-type", summary="415 Unsupported Media Type")
async def wrong_content_type(request: Request):
    """Content-Type이 application/json이 아니면 415를 반환합니다."""
    content_type = request.headers.get("content-type", "")

    if "application/json" not in content_type:
        raise HTTPException(
            status_code=415,
            detail={
                "error": "Unsupported Media Type",
                "message": f"Content-Type '{content_type}'는 지원되지 않습니다.",
                "expected": "application/json",
                "lesson": "FastAPI는 기본적으로 JSON 요청을 기대합니다. Content-Type: application/json 헤더를 포함하세요.",
            },
        )

    body = await request.json()
    return {"message": "올바른 Content-Type!", "data": body}


@router.post("/large-payload", summary="413 Payload Too Large")
async def large_payload(request: Request):
    """요청 본문이 1KB를 초과하면 413을 반환합니다."""
    body = await request.body()
    max_size = 1024  # 1KB

    if len(body) > max_size:
        raise HTTPException(
            status_code=413,
            detail={
                "error": "Payload Too Large",
                "message": f"요청 크기({len(body)} bytes)가 제한({max_size} bytes)을 초과했습니다.",
                "lesson": "서버는 보안과 성능을 위해 요청 크기를 제한할 수 있습니다. 파일 업로드 시 크기 제한을 확인하세요.",
            },
        )

    return {
        "message": "요청 크기 통과!",
        "size": len(body),
        "max_size": max_size,
    }


@router.post("/malformed-json", summary="JSON 파싱 실패")
async def malformed_json(request: Request):
    """잘못된 JSON을 보내면 파싱 에러가 발생합니다. Swagger UI에서는 정상 JSON만 전송됩니다. curl로 테스트하세요."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "JSON Parse Error",
                "message": "요청 본문이 유효한 JSON이 아닙니다.",
                "lesson": "JSON에서 흔한 실수: 작은따옴표 사용, 후행 쉼표, 따옴표 누락 등",
                "examples": {
                    "wrong": "{'name': 'Alice',}",
                    "correct": '{"name": "Alice"}',
                },
                "test_with_curl": "curl -X POST http://localhost:8000/errors/request/malformed-json -H 'Content-Type: application/json' -d '{invalid json}'",
            },
        )

    return {"message": "JSON 파싱 성공!", "data": body}


@router.get("/missing-header", summary="커스텀 헤더 누락")
def missing_header(x_api_key: str | None = Header(None)):
    """X-API-Key 헤더 없이 호출하면 에러가 발생합니다."""
    if not x_api_key:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Missing Header",
                "message": "X-API-Key 헤더가 필요합니다.",
                "lesson": "일부 API는 인증 외에도 커스텀 헤더를 요구합니다. API 문서를 꼼꼼히 확인하세요.",
                "example": "X-API-Key: your-api-key-here",
            },
        )

    return {
        "message": "API 키 확인 완료!",
        "api_key": x_api_key,
    }


@router.post("/wrong-method", summary="405 Method Not Allowed (POST만 허용)")
def wrong_method(payload: GenericPayload):
    """POST만 허용됩니다. GET으로 호출하면 FastAPI가 자동으로 405를 반환합니다."""
    return {
        "message": "POST 요청 성공!",
        "data": payload.data,
        "lesson": "HTTP 메서드(GET/POST/PUT/DELETE)를 API 문서에서 확인하세요.",
    }


@router.get("/html-instead-of-json", summary="HTML 반환 (JSON 기대)")
def html_instead_of_json():
    """JSON을 기대했지만 HTML이 반환되는 상황을 시뮬레이션합니다."""
    html = """<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body><h1>502 Bad Gateway</h1><p>nginx/1.18.0</p></body>
</html>"""
    return HTMLResponse(
        content=html,
        headers={
            "X-Lesson": "response.json() will fail on HTML. Always check Content-Type first.",
        },
    )


@router.get("/empty-response", summary="204 No Content")
def empty_response():
    """빈 응답(204)을 반환합니다. 프론트엔드에서 response.json() 호출 시 에러가 발생할 수 있습니다."""
    return Response(
        status_code=204,
        headers={
            "X-Lesson": "204 has no body. Check response.status instead of response.json().",
        },
    )


@router.get("/slow-response", summary="느린 응답")
async def slow_response(
    delay: int = Query(default=5, ge=1, le=30, description="응답 지연 시간 (초)"),
):
    """지정된 시간만큼 응답을 지연합니다. 클라이언트 타임아웃 테스트용입니다."""
    await asyncio.sleep(delay)
    return {
        "message": f"{delay}초 후 응답 완료",
        "lesson": "클라이언트에서 타임아웃을 설정하지 않으면 사용자가 오래 기다리게 됩니다. fetch의 AbortController를 활용하세요.",
    }


@router.get("/field-name-mismatch", summary="필드명 불일치 (snake_case vs camelCase)")
def field_name_mismatch():
    """Python의 snake_case와 JavaScript의 camelCase 차이를 보여줍니다."""
    return {
        "user_name": "Alice",
        "phone_number": "010-1234-5678",
        "created_at": "2024-01-15T10:30:00",
        "is_active": True,
        "lesson": "Python/FastAPI는 snake_case를 사용하지만 JavaScript에서는 camelCase가 관례입니다. 프론트에서 data.userName이 아닌 data.user_name으로 접근해야 합니다.",
        "common_mistake": "response.data.userName → undefined (올바른 접근: response.data.user_name)",
    }
