import asyncio
import websockets
import jwt, json
from datetime import datetime, timedelta

async def connect_to_room(user_id, room_key, secret_key):
    # Generate JWT token
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0MjQ4MzE4LCJpYXQiOjE3MzQxNjE5MTgsImp0aSI6IjI5YmNiODAyOGM0YjRkZWVhOWQ0ZTA4M2JhNzAzZjUyIiwidXNlcl9pZCI6NX0.xreUNNmyIiLrYblTizcpY0OXCaT3V2_LQAs51BEIrqo'
    
    # Construct WebSocket URL with token
    ws_url = f"ws://localhost:8000/ws/test/{room_key}/?token={token}"

    try:
        async with websockets.connect(ws_url) as websocket:
            print(f"User {user_id} connected to room {room_key}")

            # Send initial ready message
            await websocket.send(json.dumps({
                'type': 'ready',
                'user_id': user_id
            }))

            # Receive and print server response
            response = await websocket.recv()
            print(f"Server response: {response}")

    except Exception as e:
        print(f"Connection error: {e}")

# Example usage
async def main():
    SECRET_KEY = 'django-insecure-2_)5w)d@*9f^+ay7be!zvp%3j943^bnunxry)*lg07415(tfbt'  # Use your actual Django secret key
    user_id = 5  # The ID of the user connecting
    room_key = "PYYE9C"

    await connect_to_room(user_id, room_key, SECRET_KEY)

# Run the connection
asyncio.run(main())