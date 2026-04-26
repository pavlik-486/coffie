from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates, relationship


DATABASE = "sqlite+aiosqlite:///./database.db"
engine = create_async_engine(DATABASE, echo=True)
session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=True)
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)

    order = relationship(argument='Order', back_populates='orders') # cdzpb

    @validates('phone')
    def valid_phone(self, phone):
        cleaned = ''.join(filter(str.isdigit, phone))
        if len(cleaned) != 11:
            raise ValueError('Phone must have 11 symbols')
        if not cleaned.startswith('7') or not cleaned.startswith('8'):
            raise ValueError('Phone number can start 7 or 8')


class Order(Base):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, nullable=True, unique=True)
    user_id = Column(Integer, ForeignKey(column='users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)
    bar_id = Column(Integer, nullable=True)
    dish_id = Column(Integer, nullable=True)
    order_time = Column(String, nullable=True)
    get_order_time = Column(String, nullable=True)
    status = Column(String, nullable=True)

    user = relationship(argument='User', back_populates='users', cascade='all, delete') #связь с пользователем



# общий список кофеен, добавить связи9
class AllCoffieBars(Base):

    __tablename__ = '_all_coffie_bars'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True)
    name = Column(String, nullable=True)

#  кофейня, также нужны связи
class CoffieBar(Base):

    __tablename__ = 'coffie_bar'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True)
    name = Column(String, nullable=True)

# меню, нужны связи с кофейнями и таблицей заказов
class Menu(Base):

    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, nullable=True, unique=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=False)


#
# import asyncio
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#         print('Таблицы созданы')
#     await engine.dispose()
#
#
# if __name__ == "__main__":
#     asyncio.run(init_models(), debug=True)