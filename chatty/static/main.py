"""
ChattyApp - a world changing chat app to be acquired for billions at some
point in the future.

This is the PyScript frontend - see comments inline for how things work.

https://pyscript.net/

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

import json
from pyscript import window, when, WebSocket
from pyscript.web import page, div, img, p


socket = None  # To hold the reference for the websocket.
user_id = None  # To hold the user's name (id).
avatar_set = 1  # The avatar set to use when displaying chat messages.


def send(text):
    """
    Send a message to the server via the websocket.
    """
    if socket:
        msg = json.dumps(
            {
                "user_id": user_id,
                "message": text,
                "avatar": avatar_set,
            }
        )
        socket.send(msg)


def on_open(e):
    """
    Called when the websocket has successfully connected to the server.
    """
    send("I've connected... 👋")


def on_message(e):
    """
    Called when we receive a message from the server. The `e` event's data
    contains a strong containing the actual data.
    """
    # print(e.data)  # Log to browser console for debugging purposes.
    # The data contains a JSON payload containing the sender's name (id) and
    # the textual content of the message.
    msg = json.loads(e.data)
    sender_id = msg["user_id"]
    message = msg["message"]
    avatar = msg["avatar"]
    # Create a new div containing the correctly formatted message.
    msg_container = create_message_container(sender_id, message, avatar)
    # Add the message to the DOM.
    messages = page.find("#messages")[0]
    messages.append(msg_container)
    # That's literally all it is! :-)


def create_message_container(sender_id, message, avatar):
    """
    Create an in-memory DIV element (and associated children) to be added to
    the DOM so the message from the sender is displayed nicely in the UI.
    """
    # The containing <div/>
    msg_container = div(classes="message")
    # An avatar icon <img/> taken from robohash.
    msg_icon = img(
        src=f"https://robohash.org/{sender_id}?size=48x48&set=set{avatar}",
        classes=["avatar"],
    )
    # Hydrate the raw data into child elements of the containing <div/>
    msg_container.append(
        div(  # The left hand icon, and sender's id.
            msg_icon,
            p(sender_id, classes=["username"]),
            classes=["message_info"],
        ),
        div(  # The actual message.
            p(message, classes=["message_content"]), classes=["message_body"]
        ),
    )
    return msg_container


@when("click", "#connect")
async def connect_to_chat(e):
    """
    Called @when the initial `#connect` button is clicked.
    """
    # Ensure we have a user_id to use when sending messages to the server.
    global user_id, avatar_set
    user_id_element = page.find("#user_id")[0]
    user_id = user_id_element.value.strip()
    if not user_id:
        # Indicate a user_id is needed and return.
        user_id_element.style["background-color"] = "#faa"
        return
    avatar_element = page.find("#avatar_select")[0]
    avatar_set = int(avatar_element.value)
    # Hide the registration div, show the chat div.
    register = page.find("#register")
    chat = page.find("#chat")
    register.hidden = True
    chat.style["display"] = "flex"
    # Create the expected URL for the websocket connection.
    loc = window.location
    protocol = "wss:" if loc.protocol == "https:" else "ws:"
    url = f"{protocol}//{loc.host}/ws"
    # print(url)  # Debug to browser console to check correct value.
    # Connect to the server's web-socket, via the expected URL.
    global socket
    socket = WebSocket(url=url)
    # Connect the required event handlers.
    socket.onopen = on_open
    socket.onmessage = on_message


@when("click", "#send")
async def send_chat(e):
    """
    Called @when the `#send` button is clicked.
    """
    # Find the user's input.
    msg_input = page.find("#message-input")[0]
    # Grab their typed in message.
    msg = msg_input.value.strip()
    if not msg:
        # Indicate a message is needed and return.
        msg_input.style["background-color"] = "#faa"
        return
    # Ensure correct background if there had been a prior error.
    msg_input.style["background-color"] = "#fff"
    # Reset the message input.
    msg_input.value = ""
    # Send it to the server (which will echo it back to us).
    send(msg)
