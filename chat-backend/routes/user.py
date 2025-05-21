from flask import Blueprint, request, jsonify, session
from flask_login import login_user
import json
import datetime
from models import db, User

user_bp = Blueprint('user', __name__)

# 用户加载器
def load_user(user_id):
    return User.query.get(int(user_id))

# 注册接口
@user_bp.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    username = data.get('username')
    password = data.get('password')
    nickname = data.get('nickname', username)
    
    # 检查用户是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '用户名已存在'})
    
    # 创建新用户
    user = User(username=username, nickname=nickname)
    user.set_password(password)
    
    # 保存到数据库
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '注册成功'})

# 登录接口
@user_bp.route('/api/login', methods=['POST'])
def login():
    print("登录API被调用")
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    username = data.get('username')
    password = data.get('password')
    print(f"尝试登录用户: {username}")
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    
    # 验证密码
    if user and user.check_password(password):
        login_user(user)
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        # 存储用户信息到session
        user_data = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname
        }
        session['user'] = json.dumps(user_data)
        print(f"用户 {username} 登录成功，session设置为: {session}")
        
        return jsonify({
            'success': True,
            'user': user_data
        })
    
    print(f"用户 {username} 登录失败，密码错误或用户不存在")
    return jsonify({'success': False, 'message': '用户名或密码错误'}) 