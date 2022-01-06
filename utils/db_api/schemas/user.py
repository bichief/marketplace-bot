import datetime

from sqlalchemy import Column, Integer, BigInteger, String, sql, DateTime, func

from utils.db_api.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(BigInteger(), unique=True, nullable=False)
    username = Column(String(), unique=True)
    state = Column(String(), default='false')
    created_at = Column(DateTime(False), default=datetime.date.today(), server_default=func.now())

    query: sql.Select
