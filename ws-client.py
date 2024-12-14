import asyncio
import websockets
import jwt, json

async def connect_to_room(user_id, room_key, secret_key):
    # Generate JWT token (use your JWT generation logic here)
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0MjQ3NzMxLCJpYXQiOjE3MzQxNjEzMzEsImp0aSI6IjkzN2FkMTgzOThhNTQ5Mzk5NDFiN2ZjMDNiOTIwZmRhIiwidXNlcl9pZCI6Nn0.nXkVjBguIcAstFcMN8jXRyuh9LAvLRsz9QFmBjS5md4'
    
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
            print("Sent 'ready' message")

            # Listen for response from the server
            response = await websocket.recv()
            print(f"Server response: {response}")

            # Simulate starting the test
            await asyncio.sleep(2)  # Wait to simulate delay
            await websocket.send(json.dumps({
                'type': 'start_test',
                'user_id': user_id
            }))
            print("Sent 'start_test' message")


            response = await websocket.recv()
            print(f"Server response: {response}")
            try:
                # Simulate submitting an answer
                if "questions" in response:
                    questions = json.loads(response).get('questions', [])
                    if questions:
                        for question in questions:
                            question_id = question['id']  
                            answer_text = str(input("Give the answer : "))
                            await asyncio.sleep(2) 
                            await websocket.send(json.dumps({
                                'type': 'submit_answer',
                                'user_id': user_id,
                                'question_id': question_id,
                                'answer_text': answer_text
                            }))
                            print(f"Sent 'submit_answer' for question ID {question_id}")

                            try:
                                answer_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                                print(f"Answer submission response: {answer_response}")
                            except asyncio.TimeoutError:
                                print("Timeout waiting for answer confirmation")
            except Exception as e:
                print(f"Error processsing exam response. {e}")

    except Exception as e:
        print(f"Connection error: {e}")

# Example usage
async def main():
    SECRET_KEY = 'django-insecure-2_)5w)d@*9f^+ay7be!zvp%3j943^bnunxry)*lg07415(tfbt'  # Replace with your actual Django secret key
    user_id = 5  # The ID of the user connecting
    room_key = "TJYE5"  # Room key to join

    await connect_to_room(user_id, room_key, SECRET_KEY)

# Run the client
asyncio.run(main())
