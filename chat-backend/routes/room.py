from flask import Blueprint, request, jsonify, session
import json
from models import db, Room, UserRoom

room_bp = Blueprint('room', __name__)

# 获取用户已加入的房间
@room_bp.route('/api/user/rooms', methods=['GET'])
def get_user_rooms():
    print("获取用户房间API被调用")
    print("当前session:", session)
    
    # 从session获取用户ID
    user_id = None
    if 'user' in session:
        try:
            user_data = json.loads(session['user'])
            user_id = user_data.get('id')
            print(f"从session获取到用户ID: {user_id}")
        except Exception as e:
            print(f"解析session出错: {e}")
            return jsonify({'success': False, 'message': '未找到用户信息', 'rooms': []})
    
    if not user_id:
        print("未找到用户ID，可能未登录")
        return jsonify({'success': False, 'message': '用户未登录', 'rooms': []})
    
    # 查询用户已加入的房间
    user_rooms = UserRoom.query.filter_by(user_id=user_id).all()
    print(f"找到 {len(user_rooms)} 个用户房间关系")
    rooms = []
    
    for user_room in user_rooms:
        room = Room.query.get(user_room.room_id)
        if room:
            rooms.append({
                'id': room.id,
                'name': room.name,
                'joined_at': user_room.joined_at.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    print(f"返回房间列表: {rooms}")
    return jsonify({'success': True, 'rooms': rooms})

# 加入房间API
@room_bp.route('/api/rooms/join', methods=['POST'])
def join_room_api():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    room_name = data.get('room')
    if not room_name:
        return jsonify({'success': False, 'message': '房间名不能为空'})
    
    # 从session获取用户ID
    user_id = None
    if 'user' in session:
        try:
            user_data = json.loads(session['user'])
            user_id = user_data.get('id')
        except:
            return jsonify({'success': False, 'message': '未找到用户信息'})
    
    if not user_id:
        return jsonify({'success': False, 'message': '用户未登录'})
    
    # 保存用户-房间关系
    try:
        save_user_room_relation(user_id, room_name)
        return jsonify({'success': True, 'message': f'成功加入房间 {room_name}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'加入房间失败: {str(e)}'})

# 离开房间API
@room_bp.route('/api/rooms/leave', methods=['POST'])
def leave_room_api():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    room_name = data.get('room')
    if not room_name:
        return jsonify({'success': False, 'message': '房间名不能为空'})
    
    # 从session获取用户ID
    user_id = None
    if 'user' in session:
        try:
            user_data = json.loads(session['user'])
            user_id = user_data.get('id')
        except:
            return jsonify({'success': False, 'message': '未找到用户信息'})
    
    if not user_id:
        return jsonify({'success': False, 'message': '用户未登录'})
    
    # 删除用户-房间关系
    try:
        room = Room.query.filter_by(name=room_name).first()
        if room:
            user_room = UserRoom.query.filter_by(user_id=user_id, room_id=room.id).first()
            if user_room:
                db.session.delete(user_room)
                db.session.commit()
                return jsonify({'success': True, 'message': f'成功离开房间 {room_name}'})
            else:
                return jsonify({'success': False, 'message': '您不在该房间中'})
        else:
            return jsonify({'success': False, 'message': '房间不存在'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'离开房间失败: {str(e)}'})

# 保存用户-房间关系到数据库
def save_user_room_relation(user_id: int, room_name: str) -> Room:
    # 查找房间，使用大小写不敏感的查询
    room = Room.query.filter(Room.name.ilike(room_name)).first()
    
    # 如果找不到房间，创建新房间
    if not room:
        room = Room(name=room_name)
        db.session.add(room)
        db.session.commit()
        print(f"创建新房间: {room_name}, ID: {room.id}")
    else:
        print(f"使用现有房间: {room_name}, ID: {room.id}")
    
    # 检查用户-房间关系是否已存在
    user_room = UserRoom.query.filter_by(user_id=user_id, room_id=room.id).first()
    if not user_room:
        user_room = UserRoom(user_id=user_id, room_id=room.id)
        db.session.add(user_room)
        db.session.commit()
        print(f"为用户 {user_id} 创建与房间 {room_name} 的关系")
    else:
        print(f"用户 {user_id} 已经在房间 {room_name} 中")
    
    return room 