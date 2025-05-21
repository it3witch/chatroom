from flask_socketio import emit
from flask import session, request
import json
from models import db, Room, Message
from datetime import datetime

def init_message_events(socketio):
    @socketio.event
    def sendMsg(message):
        room = message.get('room', '')
        msg = message.get('msg', '')
        nickname = message.get('nickname', '匿名用户')
        print(f"收到消息 - 房间: {room}, 发送者: {nickname}, 内容: {msg}")
        # 如果用户已登录，保存消息到数据库
        try:
            if 'user' in session:
                user_data = json.loads(session['user'])
                user_id = user_data.get('id')
                if user_id:
                    # 获取房间ID
                    room_obj = Room.query.filter_by(name=room).first()
                    if room_obj:
                        msg_obj = Message(
                            content=msg,
                            user_id=user_id,
                            room_id=room_obj.id
                        )
                        db.session.add(msg_obj)
                        db.session.commit()
                        print(f"消息已保存到数据库 - 用户ID: {user_id}, 房间ID: {room_obj.id}")
        except Exception as e:
            print(f"保存消息出错: {e}")
        
        # 获取SocketIO连接ID
        sid = request.sid  # type: ignore
        print(f"发送者SocketID: {sid}")
        
        # 检查用户是否在房间中
        user_rooms = socketio.server.rooms(sid)
        if room not in user_rooms:
            print(f"错误：用户不在房间 {room} 中")
            return
        
        # 广播消息到房间内的所有用户
        emit('sendToAll', {
            "msg": msg,
            "user": sid,
            "nickname": nickname,
            "room": room,
            "time": datetime.now().strftime("%H:%M:%S")
        }, to=room)
        print(f"消息已广播到房间 {room}") 