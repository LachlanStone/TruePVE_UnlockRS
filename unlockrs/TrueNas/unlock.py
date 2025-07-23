import websockets
import json

async def connect_to_websocket(endpoint, username, password):
# Default Settinngs for this component
    # TODO: Implement actual websocket connection and authentication
    print(f"Attempting to connect to TrueNAS at ws://{endpoint}/websocket")
    # WebSocket Comunication Component that is being used
    async with websockets.connect(f"ws://{endpoint}/websocket") as ws:
        # Connect to the WebSocket
        await ws.send(json.dumps({"msg": "connect", "version": "1", "support": ["1"]}))
        print(await ws.recv())

        # Authenticate with WebSocket via UserPass
        await ws.send(json.dumps({"msg": "method", "id": "1", "method": "auth.login", "params": [username, password]}))
        print(await ws.recv())

        # Send Data to the WebSocket
        await ws.send(json.dumps({"msg": "method", "id": "2", "method": "core.ping"}))      
        status = json.loads(await ws.recv())["result"]
        assert status == "pong" # Confirm that Data is good as result of core.ping should allways be pong