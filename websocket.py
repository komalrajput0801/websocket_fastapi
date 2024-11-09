from fastapi import WebSocket
from utils import print_client_details


class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        """connect event"""
        print("connect called..........................")
        await websocket.accept()
        
        # if user id already exists that means same user has connected from different tab or 
        # browser, like we have opened whatsapp in browser and app both, so if msg should be 
        # sent to both of them
        if user_id in self.active_connections.keys():
            self.active_connections[user_id].append(websocket)
        else:
            self.active_connections[user_id] = [websocket]

        print("Active Connections:", self.active_connections)
        for user, conns in self.active_connections.items():
            print(f"Connections for user {user}::::")
            for conn in conns:
                print_client_details(conn)


    async def send_message(self, message: str, user_id: str):
        """Direct Message"""
        print("send message called..........................")
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id]:
                await websocket.send_text(message)
    
    async def disconnect(self, websocket: WebSocket):
        """disconnect event"""

        # update user's websocket connections by removing the websocket which was removed
        for user_id, websocket_conn in self.active_connections.items():
            if websocket in websocket_conn:
                websocket_conn.remove(websocket)
                self.active_connections[user_id] = websocket_conn
