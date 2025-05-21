from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .room import Room, UserRoom, Message 