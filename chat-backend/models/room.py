import datetime
from . import db

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Room, self).__init__(**kwargs)
    
    @classmethod
    def clean_duplicate_rooms(cls):
        """清理重复的房间记录"""
        try:
            print("检查并清理重复的房间记录...")
            # 获取所有房间名称
            room_names = db.session.query(cls.name).all()
            room_names = [r[0] for r in room_names]
            
            # 检查重复的房间名称
            duplicates = {}
            for name in room_names:
                rooms = cls.query.filter_by(name=name).all()
                if len(rooms) > 1:
                    duplicates[name] = rooms
            
            # 处理重复的房间
            for name, rooms in duplicates.items():
                print(f"发现重复房间 '{name}': {len(rooms)} 条记录")
                # 保留第一条记录，删除其他记录
                keep_room = rooms[0]
                for room in rooms[1:]:
                    # 更新用户房间关系到保留的房间
                    user_rooms = UserRoom.query.filter_by(room_id=room.id).all()
                    for user_room in user_rooms:
                        # 检查是否已经存在关系
                        existing = UserRoom.query.filter_by(
                            user_id=user_room.user_id, 
                            room_id=keep_room.id
                        ).first()
                        
                        if not existing:
                            user_room.room_id = keep_room.id
                        else:
                            db.session.delete(user_room)
                    
                    # 更新消息到保留的房间
                    messages = Message.query.filter_by(room_id=room.id).all()
                    for message in messages:
                        message.room_id = keep_room.id
                    
                    # 删除重复的房间
                    db.session.delete(room)
                
                db.session.commit()
                print(f"已清理房间 '{name}' 的重复记录")
            
            if not duplicates:
                print("未发现重复房间记录")
                
        except Exception as e:
            print(f"清理重复房间时出错: {e}")
            db.session.rollback()

class UserRoom(db.Model):
    __tablename__ = 'user_rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(UserRoom, self).__init__(**kwargs)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    user = db.relationship('User', backref='messages')
    room = db.relationship('Room', backref='messages')
    
    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs) 