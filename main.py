from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

# 静的ファイル（CSS, JS）を提供
app.mount("/static", StaticFiles(directory="static"), name="static")

# 最新のメッセージを保存
latest_message = ""

# クライアントとのWebSocket接続を管理
connections = set()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """HTMLを返す"""
    html_path = Path("templates/index.html").read_text()
    return HTMLResponse(content=html_path)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket接続を管理"""
    global latest_message
    await websocket.accept()
    connections.add(websocket)

    # クライアント接続時に最新のメッセージを送信
    await websocket.send_text(latest_message)

    try:
        while True:
            data = await websocket.receive_text()
            latest_message = data  # 最新のメッセージを更新
            for conn in connections:
                await conn.send_text(latest_message)  # 全クライアントに送信
    except:
        connections.remove(websocket)
