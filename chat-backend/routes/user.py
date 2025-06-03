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

# 更新头像接口
@user_bp.route('/api/user/avatar', methods=['POST'])
def update_avatar():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    avatar_data = data.get('avatar')
    if not avatar_data:
        return jsonify({'success': False, 'message': '头像数据不能为空'})
    
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
    
    # 更新用户头像
    try:
        user = User.query.get(user_id)
        if user:
            user.avatar = avatar_data
            db.session.commit()
            return jsonify({'success': True, 'message': '头像更新成功'})
        else:
            return jsonify({'success': False, 'message': '用户不存在'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'更新头像失败: {str(e)}'})

# 更新昵称接口
@user_bp.route('/api/user/nickname', methods=['POST'])
def update_nickname():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    new_nickname = data.get('nickname')
    if not new_nickname:
        return jsonify({'success': False, 'message': '昵称不能为空'})
    
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
    
    # 更新用户昵称
    try:
        user = User.query.get(user_id)
        if user:
            user.nickname = new_nickname
            db.session.commit()
            
            # 更新session中的用户信息
            user_data['nickname'] = new_nickname
            session['user'] = json.dumps(user_data)
            
            return jsonify({'success': True, 'message': '昵称更新成功'})
        else:
            return jsonify({'success': False, 'message': '用户不存在'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'更新昵称失败: {str(e)}'})

# 修改密码接口
@user_bp.route('/api/user/password', methods=['POST'])
def update_password():
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': '无效的请求数据'})
    
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')
    
    if not old_password or not new_password:
        return jsonify({'success': False, 'message': '密码不能为空'})
    
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
    
    # 更新用户密码
    try:
        user = User.query.get(user_id)
        if user:
            # 验证旧密码
            if not user.check_password(old_password):
                return jsonify({'success': False, 'message': '旧密码错误'})
            
            # 设置新密码
            user.set_password(new_password)
            db.session.commit()
            return jsonify({'success': True, 'message': '密码修改成功'})
        else:
            return jsonify({'success': False, 'message': '用户不存在'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'修改密码失败: {str(e)}'}) 