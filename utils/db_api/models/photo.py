from sqlalchemy import Integer, Column, ForeignKey, String, sql

from utils.db_api.base import Base

class GoodsPhoto(Base):
    __tablename__ = 'photo'

    id = Column(Integer(), primary_key=True)
    goods_id = Column(Integer(), ForeignKey('goods.id'))
    url = Column(String())

    query: sql.Select