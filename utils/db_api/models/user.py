import datetime

from sqlalchemy import Column, Integer, BigInteger, String, sql, DateTime, func
from sqlalchemy.orm import relationship

from utils.db_api.base import Base
from utils.db_api.models.balance import Balance


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger(), unique=True, nullable=False)
    username = Column(String(), unique=True)
    state = Column(String(), default='false')
    created_at = Column(DateTime(False), default=datetime.date.today(), server_default=func.now())

    balance = relationship(Balance)

    query: sql.Select
