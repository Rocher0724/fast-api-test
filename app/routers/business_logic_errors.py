"""비즈니스 로직/런타임 에러 엔드포인트 — 강의 3.2장 500 에러 연결."""

import asyncio
import sys

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/errors/logic", tags=["5. 비즈니스 로직 에러"])


@router.get("/division-by-zero", summary="ZeroDivisionError")
def division_by_zero(
    dividend: int = Query(default=100, description="나눌 수"),
    divisor: int = Query(default=0, description="나누는 수 (0이면 에러)"),
):
    """divisor=0이면 ZeroDivisionError가 발생합니다."""
    result = dividend / divisor
    return {"result": result}


@router.get("/key-error", summary="KeyError")
def key_error(
    key: str = Query(default="missing_key", description="조회할 딕셔너리 키"),
):
    """존재하지 않는 키를 조회하면 KeyError가 발생합니다."""
    data = {"name": "Alice", "age": 25, "email": "alice@example.com"}
    value = data[key]
    return {"key": key, "value": value}


@router.get("/index-error", summary="IndexError")
def index_error(
    index: int = Query(default=10, description="조회할 리스트 인덱스"),
):
    """리스트 범위를 벗어나는 인덱스를 조회하면 IndexError가 발생합니다."""
    items = ["apple", "banana", "cherry"]
    value = items[index]
    return {"index": index, "value": value}


@router.get("/type-error", summary="TypeError")
def type_error():
    """호환되지 않는 타입 간 연산으로 TypeError가 발생합니다."""
    result = "hello" + 42  # noqa: F841 — intentional error
    return {"result": result}


@router.get("/attribute-error", summary="AttributeError")
def attribute_error():
    """존재하지 않는 속성/메서드를 호출하면 AttributeError가 발생합니다."""
    data = {"name": "Alice"}
    result = data.upper()  # dict에는 upper() 메서드가 없음
    return {"result": result}


@router.get("/none-reference", summary="NoneType 에러")
def none_reference():
    """None 값에서 메서드를 호출하면 AttributeError가 발생합니다."""

    def find_user(user_id: int):
        return None  # 사용자를 찾지 못한 상황

    user = find_user(999)
    name = user.name  # None.name → AttributeError
    return {"name": name}


@router.get("/recursion-limit", summary="RecursionError")
def recursion_limit():
    """안전한 깊이 제한(50)으로 무한 재귀를 시뮬레이션합니다."""
    counter = {"depth": 0, "max_depth": 50}

    def recursive_call(n: int) -> int:
        counter["depth"] += 1
        if counter["depth"] > counter["max_depth"]:
            raise RecursionError(
                f"maximum recursion depth exceeded (안전 제한: {counter['max_depth']})"
            )
        return recursive_call(n + 1)

    recursive_call(0)


@router.get("/timeout", summary="느린 응답 시뮬레이션")
async def slow_response(
    seconds: int = Query(default=10, ge=1, le=60, description="대기 시간 (초, 최대 60)"),
):
    """지정된 시간만큼 대기합니다. 클라이언트 타임아웃을 테스트할 수 있습니다."""
    await asyncio.sleep(seconds)
    return {
        "message": f"{seconds}초 후 응답 완료",
        "lesson": "서버 응답이 느릴 때 클라이언트는 타임아웃 에러를 받을 수 있습니다. fetch의 AbortController나 axios의 timeout 설정을 확인하세요.",
    }


@router.get("/value-error", summary="ValueError")
def value_error():
    """잘못된 값 변환으로 ValueError가 발생합니다."""
    result = int("abc")
    return {"result": result}


@router.get("/unhandled-vs-handled", summary="처리/미처리 에러 비교")
def unhandled_vs_handled(
    handled: bool = Query(default=False, description="True면 에러를 잡고, False면 그대로 전파"),
):
    """handled=true면 에러를 잡아서 정상 응답, handled=false면 500 에러가 발생합니다."""
    if handled:
        try:
            result = 1 / 0
        except ZeroDivisionError:
            return {
                "message": "에러가 발생했지만 처리되었습니다!",
                "error_type": "ZeroDivisionError",
                "lesson": "try/except로 에러를 잡으면 500이 아닌 정상 응답을 반환할 수 있습니다.",
            }
    else:
        # 미처리 에러 → 500 Internal Server Error
        result = 1 / 0
        return {"result": result}
