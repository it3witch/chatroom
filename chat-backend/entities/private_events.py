from flask_socketio import emit, join_room, leave_room
from flask import session, request
import json
from models import db, room, Message
from datetime import datetime
from room_events import nickname_to_sid

def init_private_events(socketio):
    @socketio.on('start_private_chat')
    def handle_private_chat(data):
        to_user = data.get('to') # 目标方
        from_user = data.get('from') # 发起方
        print(f"{from_user} 想要和 {to_user} 私聊")
        
        room_name = generate_private_room_name(from_user, to_user)
        sid = request.sid # type: ignore
        join_room(room_name) # 发起方加入房间

        to_sid = nickname_to_sid.get(to_user)
        if to_sid:
             # 让目标用户加入该房间
            socketio.server.enter_room(to_sid, room_name)
            # 通知目标用户，告诉他有新私聊房间
            emit('private_chat_invite', {
                'room': room_name,
                'from': from_user
            }, to=to_sid)
        
        emit('private_chat_started', {
            'room': room_name,
            'to': to_user
        }, to=sid)

    def generate_private_room_name(user1, user2):
        return '_'.join(sorted([user1, user2]))