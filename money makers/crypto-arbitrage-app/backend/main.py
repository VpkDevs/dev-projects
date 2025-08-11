from fastapi import FastAPI, WebSocket
from utils.health import router as health_router

app = FastAPI()
app.include_router(health_router)

@app.get("/")
def read_root():
    return {"msg": "Crypto Arbitrage Backend Running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("WebSocket connection established.")
    await websocket.close()
