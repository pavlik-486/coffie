from sqlalchemy import Column, Integer, String
# сделать связи
from Database import Base

# общий список кофеен
class AllCoffieBars(Base):

    __tablename__ = 'coffie_bars'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True)
    name = Column(String, nullable=True)

# новая кофейня
class NewCoffieBar(Base):

    __tablename__ = None

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True)
    name = Column(String, nullable=True)

# меню для новой кофейни
class Menu(Base):

    __tablename__ = None

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=False)
