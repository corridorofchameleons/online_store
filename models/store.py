from _datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Boolean

metadata = MetaData()


users = Table(
    'items',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('price', Integer, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP),
    Column('is_active', Boolean, default=True)
)
