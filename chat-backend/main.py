import eventlet
eventlet.monkey_patch()

from flask import Flask, request, session
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_cors import CORS
from models import db, User, Room, UserRoom, Message
from routes import user_bp, room_bp
from routes.user import load_user
from entities import init_socket_events
import os

# 创建 Flask 应用
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['SECRET_KEY'] = 'bruh'  # 配置一个密钥，用于 Flask 会话
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # 设置SameSite属性
app.config['SESSION_COOKIE_SECURE'] = False  # 开发环境设为False，生产环境应为True
app.config['SESSION_COOKIE_HTTPONLY'] = True  # 防止JavaScript访问cookie

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/chat_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 配置登录管理
login_manager = LoginManager(app)
login_manager.user_loader(load_user)

# 配置CORS，确保允许凭据和所有必要的头部
CORS(app, 
    resources={r"/api/*": {"origins": "http://localhost:5173"}}, 
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# 配置Socket.IO
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(room_bp)

# 初始化Socket.IO事件
init_socket_events(socketio)

# 创建数据库表
with app.app_context():
    db.create_all()

# 路由 - 这里只提供 WebSocket，不再渲染 HTML
@app.route('/')
def main():
    return "Flask server is running, Vue handles the frontend"

# 运行应用
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
