
function connectToWebSocket(userId, roomKey, token) {
    const token = token
    const wsUrl = `ws://localhost:8000/ws/test/${roomKey}/?token=${token}`;

    const socket = new WebSocket(wsUrl);

    socket.onopen = (event) => {
        console.log(`User ${userId} connected to room ${roomKey}`);
        
        // Send initial ready message
        socket.send(JSON.stringify({
            type: 'ready',
            user_id: userId
        }));
    };

    socket.onmessage = (event) => {
        console.log('Received message:', event.data);
    };

    socket.onerror = (error) => {
        console.error('WebSocket Error:', error);
    };

    socket.onclose = (event) => {
        console.log('WebSocket connection closed');
    };

    return socket;
}

// Usage
const userId = 6;
const roomKey = "PYYE9C";
const token = '';
const socket = connectToWebSocket(userId, roomKey, token);