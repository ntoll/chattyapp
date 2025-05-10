"""
ChattyApp - a world changing chat app to be acquired for billions at some
point in the future.

This is the Quart based server that broadcasts all incoming messages to
everyone connected.

https://quart.palletsprojects.com/en/latest/

Copyright (c) 2025 Nicholas H.Tollervey and Paul Everitt.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import json
from quart import Quart, render_template, websocket


app = Quart(__name__)
connected_websockets = set()  # Holds connections.


@app.route("/", methods=["GET"])
async def home():
    """
    Just return a page that kicks off PyScript.
    """
    return await render_template("home.html")


@app.websocket("/ws")
async def ws():
    """
    Handle separate connections to the websocket endpoint. Just broadcast any
    incoming messages to everyone connected.
    """
    # Create and store a queue of messages to send to the connected client.
    queue = asyncio.Queue()
    connected_websockets.add(queue)
    # Tell the connected client the number of folks in the chat.
    others_connected = len(connected_websockets) - 1
    await queue.put(
        json.dumps(
            {
                "user_id": "ChattyApp",
                "message": f"There are {others_connected} other[s] connected.",
                "avatar": 1,
            }
        )
    )
    try:
        # Create sender and receiver tasks
        send_task = asyncio.create_task(send_handler(queue))
        receive_task = asyncio.create_task(receive_handler(queue))

        # Wait for either task to complete
        done, pending = await asyncio.wait(
            [send_task, receive_task], return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel any pending tasks
        for task in pending:
            task.cancel()
    finally:
        # Remove this connection from the set when done
        connected_websockets.remove(queue)


async def send_handler(queue):
    """
    Send messages put onto the queue to the connected client via the websocket.
    """
    while True:
        message = await queue.get()
        await websocket.send(message)


async def receive_handler(queue):
    """
    Receive messages from the WebSocket and broadcast to all clients by putting
    it on all their queues.
    """
    while True:
        # Get message from this client
        message = await websocket.receive()
        # Broadcast to all connected clients
        for other_queue in connected_websockets:
            await other_queue.put(message)
