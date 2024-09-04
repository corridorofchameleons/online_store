from _datetime import datetime, UTC

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey

metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False, unique=True),
    Column('phone', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow)
)
