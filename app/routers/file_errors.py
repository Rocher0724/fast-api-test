"""파일/리소스 에러 엔드포인트."""

import os

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/errors/file", tags=["9. 파일/리소스 에러"])


@router.get("/not-found", summary="FileNotFoundError")
def file_not_found(
    filename: str = Query(default="nonexistent.txt", description="찾을 파일명"),
):
    """존재하지 않는 파일을 읽으려 할 때 발생하는 에러입니다."""
    try:
        with open(filename) as f:
            content = f.read()
        return {"filename": filename, "content": content}
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "FileNotFoundError",
                "message": f"'{filename}' 파일을 찾을 수 없습니다.",
                "lesson": "파일 경로가 잘못되었거나 파일이 존재하지 않을 때 발생합니다. 상대 경로와 절대 경로의 차이를 이해하세요.",
                "checklist": [
                    "파일명 오타 확인",
                    "파일 경로 확인 (상대 경로 vs 절대 경로)",
                    "파일이 실제로 존재하는지 ls로 확인",
                ],
            },
        )


@router.get("/permission-denied", summary="PermissionError")
def permission_denied():
    """파일 권한 에러를 시뮬레이션합니다."""
    raise HTTPException(
        status_code=403,
        detail={
            "error": "PermissionError",
            "message": "[Errno 13] Permission denied: '/etc/shadow'",
            "lesson": "파일 읽기/쓰기 권한이 없을 때 발생합니다. chmod로 권한을 변경하거나 적절한 사용자로 실행하세요.",
            "commands": {
                "확인": "ls -la filename",
                "읽기 권한 추가": "chmod +r filename",
                "소유자 변경": "chown user:group filename",
            },
        },
    )


@router.get("/is-directory", summary="IsADirectoryError")
def is_directory():
    """디렉토리를 파일처럼 읽으려 할 때 발생하는 에러를 시뮬레이션합니다."""
    raise HTTPException(
        status_code=400,
        detail={
            "error": "IsADirectoryError",
            "message": "[Errno 21] Is a directory: './app'",
            "lesson": "디렉토리를 파일로 열려고 할 때 발생합니다. 파일 경로가 디렉토리를 가리키고 있지 않은지 확인하세요.",
        },
    )


@router.get("/encoding-error", summary="UnicodeDecodeError")
def encoding_error():
    """인코딩 에러를 시뮬레이션합니다."""
    raise HTTPException(
        status_code=400,
        detail={
            "error": "UnicodeDecodeError",
            "message": "'utf-8' codec can't decode byte 0xff in position 0: invalid start byte",
            "lesson": "파일 인코딩이 예상과 다를 때 발생합니다. EUC-KR, CP949 등 다른 인코딩을 시도하세요.",
            "solutions": [
                "open(filename, encoding='euc-kr')",
                "open(filename, encoding='cp949')",
                "open(filename, mode='rb')로 바이너리 모드로 읽기",
            ],
            "tip": "한국어 파일에서 자주 발생합니다. 특히 Windows에서 만든 파일을 Mac/Linux에서 열 때!",
        },
    )


@router.get("/path-traversal", summary="경로 순회 공격 차단")
def path_traversal(
    filename: str = Query(default="../../../etc/passwd", description="요청 파일 경로"),
):
    """경로 순회(Path Traversal) 공격을 감지하고 차단합니다."""
    # 보안: 경로 순회 감지
    normalized = os.path.normpath(filename)

    if ".." in normalized or normalized.startswith("/"):
        raise HTTPException(
            status_code=403,
            detail={
                "error": "PathTraversalBlocked",
                "message": f"경로 순회 공격이 감지되었습니다: '{filename}'",
                "normalized_path": normalized,
                "lesson": "../ 를 사용한 경로 순회 공격은 보안 위협입니다. 서버에서 반드시 경로를 정규화하고 검증해야 합니다.",
                "prevention": [
                    "os.path.normpath()로 경로 정규화",
                    "허용된 디렉토리 내부인지 확인",
                    "사용자 입력을 파일 경로에 직접 사용하지 않기",
                ],
            },
        )

    return {
        "message": "안전한 파일 경로입니다.",
        "filename": filename,
        "lesson": "이 엔드포인트는 ../를 포함한 경로를 차단합니다. 보안 테스트를 위해 ../../../etc/passwd 같은 경로를 시도해보세요.",
    }
