from flask_socketio import emit, join_room, leave_room
from flask import session, request
import json
from models import db, Room
from routes.room import save_user_room_relation

online_users = set()
sid_to_nickname = {}

def init_room_events(socketio):
    @socketio.event
    def joinRoom(message):
        room = message.get('room', '')
        nickname = message.get('nickname', '匿名用户')
        print(f"用户 {nickname} 请求加入房间: {room}")
        
        # 获取SocketIO连接ID
        sid = request.sid  # type: ignore
        
        # 检查用户是否已经在房间中
        user_rooms = socketio.server.rooms(sid)
        if room in user_rooms:
            print(f"用户 {nickname} 已经在房间 {room} 中，无需重复加入")
            return
        
        join_room(room)  # 将用户加入到指定的房间
        print(f"用户 {nickname} 已加入房间 {room}")

        # 检查用户是否已登录，存储房间关系
        try:
            if 'user' in session:
                user_data = json.loads(session['user'])
                user_id = user_data.get('id')
                if user_id:
                    save_user_room_relation(user_id, room)
        except Exception as e:
            print(f"存储房间关系出错: {e}")

        # 通知所有房间内的用户，有新用户加入（除了自己）
        emit("roomJoined", {
            "user": sid,
            "room": room,
            "type": "system",
            "message": f"{nickname} 加入了房间",
            "to": "room"  # 标记这是发给房间的消息
        }, to=room)  # 将事件发送到房间内的所有客户端

        # 通知用户自己
        emit("roomJoined", {
            "user": sid,
            "room": room,
            "type": "system",
            "message": f"你已加入房间 {room}"
            # 没有 to 参数，表示这是发给用户自己的消息
        })
        
        # 广播更新在线人数
        online_users.add(nickname)
        sid_to_nickname[sid] = nickname
        emit('update_online_users', list(online_users), broadcast=True)

    @socketio.event
    def leaveRoom(message):
        room = message.get('room', '')
        nickname = message.get('nickname', '匿名用户')
        print(f"用户 {nickname} 请求离开房间: {room}")
        
        # 获取SocketIO连接ID
        sid = request.sid  # type: ignore
        
        # 注意：这里只是离开socket连接，不应该删除数据库中的用户-房间关系
        # 只有通过API明确请求离开房间时才删除关系
        
        leave_room(room)  # 用户离开房间
        print(f"用户 {nickname} 已离开房间 {room}")
        emit('roomLeft', {'room': room, 'user': sid, 'nickname': nickname}, to=room)
        # 广播更新在线人数
        online_users.discard(nickname)
        sid_to_nickname.pop(sid, None)
        emit('update_online_users', list(online_users), broadcast=True)
    
    @socketio.event
    def disconnect():
        sid = request.sid # type: ignore
        nickname = sid_to_nickname.pop(sid, None)
        if nickname:
            print(f"用户 {nickname} 离线，SID: {sid}")
            online_users.discard(nickname)
            del sid_to_nickname[sid]
            emit('update_online_users', list(online_users), broadcast=True)
        else:
            print(f"未知用户断开连接，SID: {sid}")