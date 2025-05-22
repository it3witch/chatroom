from flask_socketio import emit, join_room, leave_room
from flask import session, request
import json
from models import db, Room, Message
from datetime import datetime

def init_private_events(socketio):
    @socketio.event
    def join_private_room(message):
        room_id = message.get('roomId', '')
        user = message.get('user', '')
        target_user = message.get('targetUser', '')
        print(f"用户 {user} 请求与 {target_user} 开始私聊")
        
        # 获取SocketIO连接ID
        sid = request.sid  # type: ignore
        
        # 检查用户是否已经在私聊房间中
        user_rooms = socketio.server.rooms(sid)
        if room_id in user_rooms:
            print(f"用户 {user} 已经在私聊房间 {room_id} 中")
            return
        
        # 将发送者加入房间
        join_room(room_id)
        print(f"用户 {user} 已加入私聊房间 {room_id}")

        # 通知房间内的所有用户
        emit("private_room_joined", {
            "roomId": room_id,
            "users": [user, target_user]
        }, to=room_id)

    @socketio.event
    def leave_private_room(message):
        room_id = message.get('roomId', '')
        user = message.get('user', '')
        print(f"用户 {user} 请求离开私聊房间: {room_id}")
        
        # 获取SocketIO连接ID
        sid = request.sid  # type: ignore
        
        leave_room(room_id)  # 用户离开房间
        print(f"用户 {user} 已离开私聊房间 {room_id}")
        
        # 通知房间内的其他用户
        emit('private_room_left', {
            'roomId': room_id,
            'user': user
        }, to=room_id) 