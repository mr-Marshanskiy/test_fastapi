from sqlalchemy import Column, String, Integer, Table, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from common.models import BaseCodeModel, BaseIdModel
from config.database import Base


class Group(BaseCodeModel):
    """
        Permission groups
    """
    __tablename__ = 'users_group'
    name = Column(String(100), nullable=False)
    users = relationship('GroupUser', backref='groups', lazy='dynamic')


class User(BaseIdModel):
    __tablename__ = 'users_user'
    username = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    groups = relationship('GroupUser', backref='users', lazy='dynamic')


class GroupUser(BaseIdModel):
    __tablename__ = 'users_group_user'
    user_id = Column(ForeignKey('users_user.id'), nullable=False)
    group_id = Column(ForeignKey('users_group.code'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', name='uix_users_user_group'),
    )
