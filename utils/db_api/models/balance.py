from sqlalchemy import Integer, Column, ForeignKey, sql, BigInteger

from utils.db_api.base import Base


class Balance(Base):
    __tablename__ = 'balance'

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(BigInteger(), ForeignKey('users.telegram_id'), unique=True)
    amount = Column(Integer(), default=0)

    query: sql.Select