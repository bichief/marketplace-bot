from sqlalchemy import Integer, Column, String, sql

from utils.db_api.base import Base


class Goods(Base):
    __tablename__ = 'goods'

    id = Column(Integer(), primary_key=True, autoincrement=False)
    category = Column(String(200))
    title = Column(String(200))
    description = Column(String())
    data = Column(String())
    price = Column(Integer())
    amount = Column(Integer())

    query: sql.Select