from sqlalchemy.dialects.postgresql import ENUM

from src.app.user.enums import UserRoleEnum
from src.core.db import db, TimestampedModel


class UserModel(TimestampedModel):
    __tablename__ = 'users'

    name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    role = db.Column(ENUM(UserRoleEnum, name='user_role_enum_type'), nullable=False)
    avatar = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)


