from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from pathlib import Path
import re

router = APIRouter(prefix="/api/lectures", tags=["Lectures"])

LECTURE_DIR = Path(__file__).resolve().parent.parent.parent / "lecture"


@router.get("/")
def list_lectures():
    """lecture/ 폴더의 마크다운 파일 목록을 반환합니다."""
    files = sorted(LECTURE_DIR.glob("*.md"))
    lectures = []
    for f in files:
        name = f.stem  # filename without .md
        if name == "CLAUDE":  # skip CLAUDE.md
            continue
        # Extract order number and title from filename like "01-에러는-어디에서-나는가"
        match = re.match(r'^(\d+|appendix-[a-z])-(.+)$', name, re.IGNORECASE)
        if match:
            order = match.group(1)
            title = match.group(2).replace('-', ' ')
        else:
            order = name
            title = name.replace('-', ' ')
        lectures.append({
            "filename": f.name,
            "stem": name,
            "order": order,
            "title": title,
        })
    return lectures


@router.get("/{filename}")
def get_lecture(filename: str):
    """마크다운 파일의 원본 내용을 반환합니다."""
    # Path traversal prevention
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=403, detail="잘못된 파일 경로입니다.")
    if not filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="마크다운 파일만 요청할 수 있습니다.")

    file_path = LECTURE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"파일을 찾을 수 없습니다: {filename}")

    content = file_path.read_text(encoding="utf-8")
    return PlainTextResponse(content)
