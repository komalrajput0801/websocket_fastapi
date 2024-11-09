from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websocket import ConnectionManager
from utils import print_client_details, get_all_tasks

import asyncio

app = FastAPI()


@app.get("/")
def index():
    return "Hello"

manager = ConnectionManager()

connected_users = {}

from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# this decorator creates a websocket endpoint, 
# websocket_endpoint is a handler that remains open allowing bidirectional communication
@app.websocket("/users/{user_id}")
async def websocket_endpoint(user_id:str, websocket: WebSocket):
    print_client_details(websocket)
    try:
        loop = asyncio.get_event_loop()
        print("Event Loop is running...........")
    except RuntimeError:
        print("No event loop found..........")    
    await manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(
                    f"Received:{data} from {websocket.scope['client']}", user_id)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)

