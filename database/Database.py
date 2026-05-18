from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Time, Enum
from sqlalchemy.orm import validates, relationship
from pathlib import Path
import enum

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "database.db"
DATABASE = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(DATABASE, echo=True)
session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()


# Регистрация пользователя
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

# Заказ
class StatusOrder(enum.Enum):
    CREATED = 'Created' # создан
    IS_PREPARING = 'Preparing' # готовится
    READY = 'Ready'
    FAILED = 'Failed' # Ошибка
    CANCELLED = 'Cancelled' # Отменен


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(column='users.id'), nullable=True)
    coffie_bar_id = Column(Integer, ForeignKey('coffie_bar.id', onupdate='CASCADE'))
    dish_id = Column(Integer, ForeignKey(column='menu.id'))
    create_time = Column(DateTime, nullable=True)
    get_order_time = Column(DateTime, nullable=True)
    status = Column(Enum(StatusOrder), nullable=True, default=StatusOrder.CREATED)

    # Связи
    user = relationship('User', back_populates='orders')
    coffie_bar = relationship('CoffieBar', back_populates='orders')
    dish = relationship('Menu', back_populates='orders')


# Кофейня
class CoffieBar(Base):
    __tablename__ = 'coffie_bar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=True)
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    sum_income = Column(Integer, default=0)

    orders = relationship('Order', back_populates='coffie_bar', cascade='all, delete')
    menu_items = relationship('Menu', back_populates='coffie_bar', cascade='all, delete')


# Menu
class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, autoincrement=True)
    coffie_bar_id = Column(Integer, ForeignKey('coffie_bar.id', ondelete='CASCADE'))
    name = Column(String, nullable=True)
    photo = Column(String)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=True)

    coffie_bar = relationship('CoffieBar', back_populates='menu_items')
    orders = relationship('Order', back_populates='dish', )


# Транзакции
class Type(enum.Enum):
    DEPOSIT = 'deposit' # пополнение
    WITHDRAWAL = 'withdrawal' # списание
    TRANSFER = 'transfer' # перевод

class StatusTransaction(enum.Enum):
    PENDING = 'pending' # в обработке
    SUCCESS = 'success' # успешно
    FAILED = 'failed' # Ошибка
    CANCELLED = 'cancelled' # Отменено


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(Enum(Type), nullable=True)
    status = Column(Enum(StatusTransaction), nullable=True)
    meta_data = Column(String)



import asyncio

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_models())