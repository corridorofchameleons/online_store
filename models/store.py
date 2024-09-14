from _datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, UniqueConstraint

from models.users import users

metadata = MetaData()


items = Table(
    'items',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('price', Integer, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP, onupdate=datetime.utcnow),
    Column('is_active', Boolean, default=True)
)


cart = Table(
    'cart',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey(users.c.id, ondelete='CASCADE'), nullable=False),
    Column('item_id', Integer, ForeignKey('items.id', ondelete='CASCADE'), nullable=False),
    Column('qty', Integer, default=1),

    UniqueConstraint('user_id', 'item_id')
)
