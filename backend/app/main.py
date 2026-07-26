import time
import sys
from pathlib import Path
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Ensure the root project directory is on PYTHONPATH for importing clean modules
root_dir = Path(__file__).resolve().parents[2]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from config.settings import settings
from api.router import router as api_router
from api.graphql import router as graphql_router
from api.websockets import ws_manager

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="KALKI AI (v2.0) — Master Intelligence Operating System Gateway"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Latency Measurement Middleware
@app.middleware("http")
async def add_latency_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time_ms = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(process_time_ms)
    response.headers["X-Kalki-Version"] = settings.VERSION
    return response

# Root Route & Healthcheck
@app.get("/", tags=["System"])
async def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "OPERATIONAL",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/health", tags=["System"])
async def health():
    return {
        "status": "HEALTHY",
        "timestamp": time.time(),
        "latency_target": "<500ms"
    }

# Include REST Routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Include GraphQL Router
app.include_router(graphql_router, prefix="/graphql", tags=["GraphQL"])

# Include Real-Time WebSockets Router
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await ws_manager.connect(session_id, websocket)
    try:
        while True:
            # Maintain connection, handle client pings
            data = await websocket.receive_text()
            # Send echoed ack back to confirm client heartbeat
            await ws_manager.send_personal_message(
                {"event": "HEARTBEAT_ACK", "client_data": data}, 
                websocket
            )
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id, websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
