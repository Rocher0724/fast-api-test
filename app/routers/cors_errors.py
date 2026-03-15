"""CORS 에러 데모 엔드포인트 — 강의 5.1장 연결.

JSONResponse를 직접 반환하여 CORS 미들웨어를 우회합니다.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter(prefix="/errors/cors", tags=["6. CORS 에러"])


@router.get("/no-headers", summary="CORS 헤더 없는 응답")
def no_headers():
    """CORS 헤더 없이 응답합니다. 다른 Origin에서 fetch하면 브라우저가 차단합니다."""
    return JSONResponse(
        content={
            "message": "이 응답에는 CORS 헤더가 없습니다.",
            "lesson": "Access-Control-Allow-Origin 헤더가 없으면 브라우저가 응답을 차단합니다.",
        },
        headers={"X-No-CORS": "true"},
    )


@router.get("/wrong-origin", summary="잘못된 Origin 허용")
def wrong_origin():
    """특정 Origin만 허용합니다. 다른 Origin에서 요청하면 차단됩니다."""
    return JSONResponse(
        content={
            "message": "이 응답은 https://allowed-origin.com만 허용합니다.",
            "lesson": "Access-Control-Allow-Origin에 명시되지 않은 Origin은 차단됩니다.",
        },
        headers={
            "Access-Control-Allow-Origin": "https://allowed-origin.com",
        },
    )


@router.get("/no-methods", summary="허용 메서드 제한")
def no_methods():
    """GET만 허용하는 CORS 설정입니다. POST 등은 차단됩니다."""
    return JSONResponse(
        content={
            "message": "이 응답은 GET 메서드만 허용합니다.",
            "lesson": "Access-Control-Allow-Methods에 없는 메서드로 요청하면 CORS 에러가 발생합니다.",
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
        },
    )


@router.options("/preflight-fail", summary="Preflight 실패")
@router.get("/preflight-fail", summary="Preflight 실패 (GET)")
def preflight_fail():
    """OPTIONS 요청에 올바른 CORS 헤더를 반환하지 않아 Preflight가 실패합니다."""
    return JSONResponse(
        content={
            "message": "Preflight 요청이 이 엔드포인트에 도달했습니다.",
            "lesson": "브라우저는 특정 조건(커스텀 헤더, Content-Type: application/json 등)에서 Preflight OPTIONS 요청을 먼저 보냅니다.",
        },
        # CORS 헤더 없음 → Preflight 실패
    )


@router.get("/correct", summary="올바른 CORS 설정")
def correct_cors():
    """올바른 CORS 헤더가 포함된 응답입니다. 비교용으로 사용하세요."""
    return JSONResponse(
        content={
            "message": "이 응답은 올바른 CORS 설정을 가지고 있습니다.",
            "lesson": "Access-Control-Allow-Origin, Methods, Headers가 모두 올바르게 설정되어 있습니다.",
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


@router.get("/test-page", summary="CORS 테스트 HTML 페이지", response_class=HTMLResponse)
def test_page(request: Request):
    """브라우저에서 직접 열어 CORS 에러를 테스트할 수 있는 HTML 페이지입니다."""
    base_url = str(request.base_url).rstrip("/")
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CORS 에러 테스트</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #1a1a2e; color: #eee; }}
        h1 {{ color: #e94560; }}
        .btn {{ background: #0f3460; color: white; border: none; padding: 10px 20px; margin: 5px; cursor: pointer; border-radius: 6px; font-size: 14px; }}
        .btn:hover {{ background: #16213e; }}
        #result {{ background: #16213e; padding: 15px; border-radius: 8px; margin-top: 20px; white-space: pre-wrap; font-family: monospace; min-height: 100px; font-size: 13px; }}
        .success {{ color: #4ecca3; }}
        .error {{ color: #e94560; }}
        .info {{ color: #a8a8a8; font-size: 12px; margin-top: 5px; }}
    </style>
</head>
<body>
    <h1>CORS 에러 테스트</h1>
    <p>각 버튼을 클릭하여 다양한 CORS 상황을 테스트하세요. 브라우저 DevTools의 Console과 Network 탭도 함께 확인하세요.</p>

    <button class="btn" onclick="testCors('/errors/cors/no-headers')">CORS 헤더 없음</button>
    <button class="btn" onclick="testCors('/errors/cors/wrong-origin')">잘못된 Origin</button>
    <button class="btn" onclick="testCors('/errors/cors/no-methods')">메서드 제한</button>
    <button class="btn" onclick="testCorsPost('/errors/cors/preflight-fail')">Preflight 실패</button>
    <button class="btn" onclick="testCors('/errors/cors/correct')">올바른 CORS</button>

    <p class="info">이 페이지는 서버에서 직접 제공되므로 Same-Origin입니다. CORS 에러를 보려면 다른 포트에서 열거나, DevTools Console에서 직접 fetch를 실행하세요.</p>

    <div id="result">결과가 여기에 표시됩니다...</div>

    <script>
        const resultDiv = document.getElementById('result');

        async function testCors(path) {{
            resultDiv.innerHTML = `<span>요청 중: GET ${{path}}...</span>`;
            try {{
                const res = await fetch('{base_url}' + path);
                const data = await res.json();
                resultDiv.innerHTML = `<span class="success">성공!</span>\\n` + JSON.stringify(data, null, 2);
            }} catch (e) {{
                resultDiv.innerHTML = `<span class="error">에러 발생!</span>\\n${{e.message}}\\n\\n브라우저 DevTools Console에서 자세한 CORS 에러 메시지를 확인하세요.`;
            }}
        }}

        async function testCorsPost(path) {{
            resultDiv.innerHTML = `<span>요청 중: POST ${{path}} (Preflight 발생)...</span>`;
            try {{
                const res = await fetch('{base_url}' + path, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ test: true }})
                }});
                const data = await res.json();
                resultDiv.innerHTML = `<span class="success">성공!</span>\\n` + JSON.stringify(data, null, 2);
            }} catch (e) {{
                resultDiv.innerHTML = `<span class="error">에러 발생!</span>\\n${{e.message}}\\n\\nPreflight (OPTIONS) 요청이 실패했습니다.\\n브라우저 DevTools Network 탭에서 OPTIONS 요청을 확인하세요.`;
            }}
        }}
    </script>
</body>
</html>"""
    return HTMLResponse(content=html)
