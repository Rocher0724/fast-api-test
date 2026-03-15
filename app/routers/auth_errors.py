"""인증/인가 에러 엔드포인트 — 401 vs 403 학습.

base64 인코딩 토큰 + 인메모리 dict로 구현 (외부 라이브러리 불필요).
"""

import base64
import time
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/errors/auth", tags=["4. 인증/인가 에러"])

# ── 인메모리 사용자/토큰 저장소 ────────────────────────────────
_users_db: dict[str, str] = {
    "admin": "admin123",
    "user": "user123",
}

_tokens_db: dict[str, dict] = {}  # token -> {"username": ..., "role": ..., "created_at": ...}


# ── 모델 ───────────────────────────────────────────────────────
class LoginPayload(BaseModel):
    username: str
    password: str


# ── 헬퍼 ───────────────────────────────────────────────────────
def _create_token(username: str) -> str:
    payload = f"{username}:{time.time()}"
    return base64.b64encode(payload.encode()).decode()


def _verify_token(authorization: Optional[str]) -> dict:
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "Unauthorized",
                "message": "Authorization 헤더가 없습니다.",
                "lesson": "보호된 API에 접근하려면 Authorization: Bearer <token> 헤더가 필요합니다.",
                "example": "Authorization: Bearer eyJ1c2VyOi...",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(
            status_code=401,
            detail={
                "error": "Unauthorized",
                "message": "Authorization 헤더 형식이 잘못되었습니다.",
                "lesson": "'Bearer <token>' 형식이어야 합니다. 'Bearer' 접두사를 빼먹지 않았는지 확인하세요.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]
    token_data = _tokens_db.get(token)

    if not token_data:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "Unauthorized",
                "message": "유효하지 않은 토큰입니다.",
                "lesson": "토큰이 만료되었거나 서버에 존재하지 않습니다. 다시 로그인하세요.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data


# ── 엔드포인트 ─────────────────────────────────────────────────
@router.post("/login", summary="로그인 (토큰 발급)")
def login(payload: LoginPayload):
    """admin/admin123 또는 user/user123으로 로그인합니다."""
    stored_password = _users_db.get(payload.username)

    if not stored_password or stored_password != payload.password:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "Unauthorized",
                "message": "사용자명 또는 비밀번호가 올바르지 않습니다.",
                "lesson": "보안을 위해 '사용자명이 틀렸는지' vs '비밀번호가 틀렸는지' 구분하지 않습니다.",
                "hint": "admin/admin123 또는 user/user123으로 시도하세요.",
            },
        )

    token = _create_token(payload.username)
    role = "admin" if payload.username == "admin" else "user"
    _tokens_db[token] = {
        "username": payload.username,
        "role": role,
        "created_at": time.time(),
    }

    return {
        "message": "로그인 성공!",
        "token": token,
        "token_type": "Bearer",
        "usage": f"Authorization: Bearer {token}",
        "lesson": "이 토큰을 다른 /errors/auth 엔드포인트의 Authorization 헤더에 사용하세요.",
    }


@router.get("/protected", summary="보호된 엔드포인트 (401)")
def protected(authorization: Optional[str] = Header(None)):
    """Authorization 헤더 없이 호출하면 401이 발생합니다."""
    token_data = _verify_token(authorization)
    return {
        "message": f"환영합니다, {token_data['username']}님!",
        "role": token_data["role"],
        "lesson": "Authorization 헤더에 유효한 토큰을 보내야 접근할 수 있습니다.",
    }


@router.get("/invalid-token", summary="잘못된 토큰 (401)")
def invalid_token(authorization: Optional[str] = Header(None)):
    """잘못된 토큰을 보내면 401이 발생합니다. Authorization: Bearer invalid_token_here"""
    token_data = _verify_token(authorization)
    return {
        "message": f"토큰 유효! 사용자: {token_data['username']}",
    }


@router.get("/expired-token", summary="만료된 토큰 (401)")
def expired_token(authorization: Optional[str] = Header(None)):
    """이 엔드포인트는 토큰을 항상 만료된 것으로 처리합니다."""
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "Unauthorized",
                "message": "Authorization 헤더가 없습니다.",
                "lesson": "먼저 /errors/auth/login으로 토큰을 발급받으세요.",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    raise HTTPException(
        status_code=401,
        detail={
            "error": "TokenExpired",
            "message": "토큰이 만료되었습니다.",
            "lesson": "토큰에는 만료 시간이 있습니다. JWT에서는 exp 클레임으로 관리합니다. 만료 시 재로그인이 필요합니다.",
            "solution": "refresh token을 사용하거나 다시 로그인하세요.",
        },
        headers={"WWW-Authenticate": "Bearer error=\"token_expired\""},
    )


@router.get("/admin-only", summary="관리자 전용 (403)")
def admin_only(authorization: Optional[str] = Header(None)):
    """일반 사용자(user)로 접근하면 403, 관리자(admin)면 성공합니다."""
    token_data = _verify_token(authorization)

    if token_data["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail={
                "error": "Forbidden",
                "message": f"'{token_data['username']}'은 관리자 권한이 없습니다.",
                "lesson": "401(인증 필요)과 403(권한 부족)의 차이: 401은 '누구세요?', 403은 '당신은 안 됩니다'.",
                "your_role": token_data["role"],
                "required_role": "admin",
            },
        )

    return {
        "message": f"관리자 {token_data['username']}님, 환영합니다!",
        "secret_data": "관리자만 볼 수 있는 비밀 데이터입니다.",
        "lesson": "admin 계정으로 로그인한 토큰만 이 엔드포인트에 접근할 수 있습니다.",
    }


@router.post("/wrong-password", summary="비밀번호 틀림 (401)")
def wrong_password(payload: LoginPayload):
    """일부러 틀린 비밀번호를 보내서 로그인 실패를 체험합니다."""
    stored_password = _users_db.get(payload.username)

    if stored_password and stored_password == payload.password:
        return {
            "message": "비밀번호가 맞습니다! 이 엔드포인트는 틀린 비밀번호를 테스트하기 위한 것입니다.",
            "hint": "일부러 틀린 비밀번호를 보내보세요.",
        }

    raise HTTPException(
        status_code=401,
        detail={
            "error": "Unauthorized",
            "message": "사용자명 또는 비밀번호가 올바르지 않습니다.",
            "lesson": "로그인 실패 시 어떤 필드가 틀렸는지 알려주지 않는 것이 보안 모범 사례입니다.",
            "security_note": "'사용자명이 없습니다'라고 알려주면 공격자가 유효한 사용자명을 파악할 수 있습니다.",
        },
    )
