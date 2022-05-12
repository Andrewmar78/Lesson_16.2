from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, CheckConstraint, Date, ForeignKey
from sqlalchemy.orm import relationship, session

from utils import get_users_all, get_offers_all, get_orders_all
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """Создание модели User"""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    age = Column(Integer, CheckConstraint("age>0"))
    email = Column(String(50))
    role = Column(String(50))
    phone = Column(String(50))


class Order(db.Model):
    """Создание модели Order"""
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    address = Column(String(100))
    price = Column(Integer)
    customer_id = Column(Integer, ForeignKey("user.id"))
    executor_id = Column(Integer, ForeignKey("user.id"))
    customer = relationship("User", foreign_keys=[customer_id])
    executor = relationship("User", foreign_keys=[executor_id])


class Offer(db.Model):
    """Создание модели Offer"""
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    executor_id = Column(Integer, ForeignKey("user.id"))
    order = relationship("Order", foreign_keys=[order_id])
    executor = relationship("User", foreign_keys=[executor_id])


def fulfill_users_data():
    """Заполнение таблицы пользователей"""
    new_users = []
    for user in get_users_all():
        new_users.append(
            User(
                id=user["id"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                age=user["age"],
                email=user["email"],
                role=user["role"],
                phone=user["phone"],
            )
        )
        with session.begin():
            session.add_all(new_users)


def fulfill_orders_data():
    """Заполнение таблицы заказов"""
    new_orders = []
    for order in get_orders_all():
        new_orders.append(
            Order(
                id=order["id"],
                name=order["name"],
                description=order["description"],
                start_date=datetime.strptime(order["start_date"], '%m/%d/%Y'),
                end_date=datetime.strptime(order["end_date"], '%m/%d/%Y'),
                address=order["address"],
                price=order["price"],
                customer_id=order["customer_id"],
                executor_id=order["executor_id"],
            )
        )
        with session.begin():
            session.add_all(new_orders)


def fulfill_offers_data():
    """Заполнение таблицы предложений"""
    new_offers = []
    for offer in get_offers_all():
        new_offers.append(
            Offer(
                id=offer["id"],
                order_id=offer["order_id"],
                executor_id=offer["executor_id"],
            )
        )
        with session.begin():
            session.add_all(new_offers)


"""Создание и заполнение таблиц"""
db.drop_all()
db.create_all()
fulfill_users_data()
fulfill_orders_data()
fulfill_offers_data()
