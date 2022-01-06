from sqlalchemy import Integer, Column, ForeignKey, sql

from utils.db_api.base import Base


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer(), primary_key=True)
    goods_id = Column(Integer(), ForeignKey('goods.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))

    query: sql.Select