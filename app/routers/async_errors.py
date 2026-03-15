"""비동기 에러 엔드포인트 — asyncio 관련 에러 학습."""

import asyncio
import time

from fastapi import APIRouter, Query

router = APIRouter(prefix="/errors/async", tags=["8. 비동기 에러"])

# ── 인메모리 상태 ──────────────────────────────────────────────
_concurrent_counter = 0
_counter_lock = None  # lazy init


# ── 엔드포인트 ─────────────────────────────────────────────────
@router.get("/timeout", summary="asyncio.TimeoutError")
async def async_timeout(
    seconds: float = Query(default=5.0, ge=0.1, le=30, description="작업 시간 (초)"),
    timeout: float = Query(default=1.0, ge=0.1, le=10, description="타임아웃 (초)"),
):
    """작업 시간이 타임아웃보다 길면 asyncio.TimeoutError가 발생합니다."""
    try:
        await asyncio.wait_for(asyncio.sleep(seconds), timeout=timeout)
        return {
            "message": f"{seconds}초 작업이 {timeout}초 안에 완료되었습니다.",
        }
    except asyncio.TimeoutError:
        return {
            "error": "asyncio.TimeoutError",
            "message": f"{seconds}초 작업이 {timeout}초 타임아웃을 초과했습니다.",
            "lesson": "asyncio.wait_for()로 비동기 작업에 타임아웃을 설정할 수 있습니다. DB 쿼리나 외부 API 호출에 필수적입니다.",
            "code_example": "await asyncio.wait_for(slow_operation(), timeout=5.0)",
        }


@router.get("/blocking-call", summary="이벤트 루프 블로킹")
async def blocking_call(
    seconds: float = Query(default=2.0, ge=0.1, le=5, description="블로킹 시간 (초)"),
):
    """time.sleep()으로 이벤트 루프를 블로킹합니다. 다른 요청도 멈추게 됩니다."""
    start = time.time()

    # 의도적으로 블로킹 호출 사용
    time.sleep(seconds)

    elapsed = time.time() - start
    return {
        "message": f"time.sleep({seconds})으로 {elapsed:.2f}초 동안 이벤트 루프가 블로킹되었습니다.",
        "lesson": "async 함수 안에서 time.sleep() 같은 블로킹 호출을 하면 전체 이벤트 루프가 멈춥니다.",
        "wrong": "time.sleep(5)  # 이벤트 루프 블로킹!",
        "correct": "await asyncio.sleep(5)  # 비블로킹",
        "for_cpu_bound": "await asyncio.to_thread(cpu_heavy_function)  # 스레드에서 실행",
    }


@router.post("/concurrent-counter", summary="Race Condition 시뮬레이션")
async def concurrent_counter(
    use_lock: bool = Query(default=False, description="True면 Lock 사용"),
):
    """동시 요청 시 카운터 불일치(Race Condition)를 시뮬레이션합니다."""
    global _concurrent_counter, _counter_lock

    if _counter_lock is None:
        _counter_lock = asyncio.Lock()

    if use_lock:
        async with _counter_lock:
            current = _concurrent_counter
            await asyncio.sleep(0.1)  # 시뮬레이션 지연
            _concurrent_counter = current + 1
    else:
        current = _concurrent_counter
        await asyncio.sleep(0.1)  # 시뮬레이션 지연 — race condition 발생 가능
        _concurrent_counter = current + 1

    return {
        "counter": _concurrent_counter,
        "used_lock": use_lock,
        "lesson": "Lock 없이 여러 요청이 동시에 같은 변수를 수정하면 Race Condition이 발생합니다.",
        "hint": "여러 터미널에서 동시에 POST 요청을 보내면 카운터 불일치를 확인할 수 있습니다.",
        "test_command": "for i in $(seq 1 10); do curl -X POST 'http://localhost:8000/errors/async/concurrent-counter' & done",
    }


@router.get("/gather-partial-failure", summary="부분 실패 (gather)")
async def gather_partial_failure():
    """3개의 비동기 작업 중 1개가 실패하는 상황을 시뮬레이션합니다."""

    async def task_success(name: str, delay: float):
        await asyncio.sleep(delay)
        return {"task": name, "status": "success"}

    async def task_fail(name: str, delay: float):
        await asyncio.sleep(delay)
        raise ValueError(f"{name} 작업 실패!")

    results = await asyncio.gather(
        task_success("작업A", 0.1),
        task_fail("작업B", 0.2),
        task_success("작업C", 0.3),
        return_exceptions=True,
    )

    formatted = []
    for r in results:
        if isinstance(r, Exception):
            formatted.append({"status": "error", "error": str(r)})
        else:
            formatted.append(r)

    return {
        "results": formatted,
        "lesson": "asyncio.gather(return_exceptions=True)를 사용하면 일부 작업이 실패해도 나머지 결과를 받을 수 있습니다.",
        "without_return_exceptions": "return_exceptions=False(기본값)이면 첫 번째 에러에서 전체가 실패합니다.",
    }


@router.get("/cancelled", summary="Task 취소 (CancelledError)")
async def cancelled_task():
    """비동기 태스크를 생성하고 즉시 취소하여 CancelledError를 시뮬레이션합니다."""

    async def long_running_task():
        try:
            await asyncio.sleep(100)
        except asyncio.CancelledError:
            return "cancelled"
        return "completed"

    task = asyncio.create_task(long_running_task())
    await asyncio.sleep(0.05)  # 잠시 대기
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

    return {
        "message": "태스크가 취소되었습니다.",
        "lesson": "task.cancel()로 비동기 태스크를 취소할 수 있습니다. 취소 시 CancelledError가 발생합니다.",
        "best_practice": "CancelledError를 잡아서 리소스 정리(cleanup) 코드를 실행하세요.",
        "code_example": "try:\n    await task\nexcept asyncio.CancelledError:\n    # cleanup 코드",
    }
