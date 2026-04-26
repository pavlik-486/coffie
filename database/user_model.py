from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates, relationship

from database.Database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=True)
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)

    order = relationship(argument='Order', back_populates='orders')

    @validates('phone')
    def valid_phone(self, phone):
        cleaned = ''.join(filter(str.isdigit, phone))
        if len(cleaned) != 11:
            raise ValueError('Phone must have 11 symbols')
        if not cleaned.startswith('7') or not cleaned.startswith('8'):
            raise ValueError('Phone number can start 7 or 8')
