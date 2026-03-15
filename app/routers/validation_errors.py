"""Pydantic 유효성 검사 에러 엔드포인트 — 강의 3.2장 연결."""

import re
from typing import Optional

from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field, field_validator

router = APIRouter(prefix="/errors/validation", tags=["2. 유효성 검사 에러"])


# ── 모델 ───────────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    age: int
    email: str


class StringConstraintsModel(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    bio: str = Field(min_length=10, max_length=200)


class NumberRangeModel(BaseModel):
    age: int = Field(ge=0, le=150)
    score: float = Field(ge=0.0, le=100.0)
    quantity: int = Field(gt=0, le=1000)


class Address(BaseModel):
    city: str
    zipcode: str = Field(pattern=r"^\d{5}$")


class NestedModel(BaseModel):
    name: str
    address: Address


class EmailModel(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError(
                "올바른 이메일 형식이 아닙니다. 예: user@example.com"
            )
        return v


class ListItemsModel(BaseModel):
    tags: list[str] = Field(min_length=1)
    scores: list[int] = Field(min_length=1)


# ── 엔드포인트 ─────────────────────────────────────────────────
@router.post("/missing-field", summary="필수 필드 누락 에러")
def missing_field(payload: UserCreate):
    """name, age, email 모두 필수입니다. 하나라도 빠지면 422가 발생합니다."""
    return {
        "message": "모든 필드가 정상적으로 전달되었습니다.",
        "data": payload.model_dump(),
        "lesson": "422 에러의 detail[].loc 배열에서 어떤 필드가 누락되었는지 확인할 수 있습니다.",
    }


@router.post("/wrong-type", summary="타입 불일치 에러")
def wrong_type(payload: UserCreate):
    """age에 문자열(예: \"twenty\")을 보내면 타입 변환 실패로 422가 발생합니다."""
    return {
        "message": "타입 검증 통과!",
        "data": payload.model_dump(),
        "lesson": "Pydantic은 자동 타입 변환을 시도하지만, 변환 불가능한 값은 422를 발생시킵니다.",
    }


@router.post("/string-constraints", summary="문자열 제약 조건 에러")
def string_constraints(payload: StringConstraintsModel):
    """username은 3~20자 영숫자/밑줄, bio는 10~200자입니다."""
    return {
        "message": "문자열 제약 조건 통과!",
        "data": payload.model_dump(),
        "lesson": "Field의 min_length, max_length, pattern으로 문자열을 제한할 수 있습니다.",
    }


@router.post("/number-range", summary="숫자 범위 초과 에러")
def number_range(payload: NumberRangeModel):
    """age: 0~150, score: 0~100, quantity: 1~1000 범위여야 합니다."""
    return {
        "message": "숫자 범위 검증 통과!",
        "data": payload.model_dump(),
        "lesson": "Field의 ge, le, gt, lt로 숫자 범위를 제한할 수 있습니다.",
    }


@router.post("/nested-model", summary="중첩 모델 유효성 에러")
def nested_model(payload: NestedModel):
    """address.zipcode는 5자리 숫자여야 합니다. 중첩 에러의 loc 경로를 확인하세요."""
    return {
        "message": "중첩 모델 검증 통과!",
        "data": payload.model_dump(),
        "lesson": "중첩 모델 에러는 detail[].loc에 ['body', 'address', 'zipcode']처럼 깊은 경로가 표시됩니다.",
    }


@router.post("/email-format", summary="이메일 형식 에러")
def email_format(payload: EmailModel):
    """올바른 이메일 형식(user@example.com)을 입력해야 합니다."""
    return {
        "message": "이메일 형식 검증 통과!",
        "data": payload.model_dump(),
        "lesson": "field_validator를 사용하여 커스텀 유효성 검사를 추가할 수 있습니다.",
    }


@router.post("/list-items", summary="빈 리스트 에러")
def list_items(payload: ListItemsModel):
    """tags와 scores는 최소 1개 이상의 항목이 있어야 합니다."""
    return {
        "message": "리스트 검증 통과!",
        "data": payload.model_dump(),
        "lesson": "Field(min_length=1)로 빈 리스트를 방지할 수 있습니다.",
    }


@router.get("/query-params", summary="쿼리 파라미터 유효성 에러")
def query_params(
    page: int = Query(ge=1, description="페이지 번호 (1 이상)"),
    size: int = Query(ge=1, le=100, description="페이지 크기 (1~100)"),
    sort: str = Query(pattern=r"^(asc|desc)$", description="정렬 방향 (asc 또는 desc)"),
):
    """쿼리 파라미터도 Pydantic이 검증합니다. 잘못된 값을 보내면 422가 발생합니다."""
    return {
        "message": "쿼리 파라미터 검증 통과!",
        "page": page,
        "size": size,
        "sort": sort,
        "lesson": "Body뿐 아니라 Query, Path 파라미터도 FastAPI가 자동 검증합니다.",
    }


@router.get("/path-params/{id}", summary="경로 파라미터 유효성 에러")
def path_params(
    id: int = Path(ge=1, le=10000, description="리소스 ID (1~10000)"),
):
    """경로 파라미터에 문자열이나 범위 밖의 숫자를 넣으면 422가 발생합니다."""
    return {
        "message": "경로 파라미터 검증 통과!",
        "id": id,
        "lesson": "Path 파라미터도 타입과 범위를 검증합니다. /path-params/abc 같은 요청은 422를 발생시킵니다.",
    }
