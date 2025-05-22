from .room_events import init_room_events
from .message_events import init_message_events
from .private_events import init_private_events

def init_socket_events(socketio):
    init_room_events(socketio)
    init_message_events(socketio) 
    init_private_events(socketio)
