from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates, relationship
from pathlib import Path

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "database.db"
DATABASE = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE, echo=True)
session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)

    # Связь с заказами
    orders = relationship('Order', back_populates='user', cascade='all, delete')

    @validates('phone')
    def valid_phone(self, key, phone):
        if phone:
            cleaned = ''.join(filter(str.isdigit, phone))
            if len(cleaned) != 11:
                raise ValueError('Phone must have 11 symbols')
            if not (cleaned.startswith('7') or cleaned.startswith('8')):
                raise ValueError('Phone number must start with 7 or 8')
            return cleaned



class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    coffie_bar_id = Column(Integer, ForeignKey('coffie_bar.id', ondelete='CASCADE', onupdate='CASCADE'))
    dish_id = Column(Integer, ForeignKey('menu.id', ondelete='CASCADE'))
    order_time = Column(String, nullable=True)
    get_order_time = Column(String, nullable=True)
    status = Column(String, nullable=True)

    # Связи
    user = relationship('User', back_populates='orders')
    coffie_bar = relationship('CoffieBar', back_populates='orders')
    dish = relationship('Menu', back_populates='orders')


class CoffieBar(Base):
    __tablename__ = 'coffie_bar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)

    # Связи
    orders = relationship('Order', back_populates='coffie_bar', cascade='all, delete')
    menu_items = relationship('Menu', back_populates='coffie_bar', cascade='all, delete')


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    coffie_bar_id = Column(Integer, ForeignKey('coffie_bar.id', ondelete='CASCADE'))
    name = Column(String, nullable=True)
    description = Column(String, nullable=False)

    # Связи
    coffie_bar = relationship('CoffieBar', back_populates='menu_items')
    orders = relationship('Order', back_populates='dish', )

#
# import asyncio
#
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     await engine.dispose()
#
#
# if __name__ == "__main__":
#     asyncio.run(init_models())