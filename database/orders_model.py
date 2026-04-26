# таблица заказов
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.Database import Base



class Order(Base):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, nullable=True, unique=True)
    user_id = Column(Integer, ForeignKey(column='users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    bar_id = Column(Integer, nullable=True)
    dish_id = Column(Integer, nullable=True)
    order_time = Column(String, nullable=True)
    get_order_time = Column(String, nullable=True)
    status = Column(String, nullable=True)

    user = relationship(argument='User', back_populates='users', cascade='all, delete')

    # сделать связи
