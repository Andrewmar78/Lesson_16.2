from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils import get_users_all, get_offers_all, get_orders_all
from main import db
from datetime import datetime


class User(db.Model):
    """Создание модели User"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint("age>0"))
    email = db.Column(db.String(50))
    # Надо бы как-то добавить проверку на содержание собаки в почте и наличия только одной из двух ролей...
    role = db.Column(db.String(50))
    phone = db.Column(db.String(50))


class Order(db.Model):
    """Создание модели Order"""
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    customer = db.relationship("User", foreign_keys=[customer_id])
    executor = db.relationship("User", foreign_keys=[executor_id])


class Offer(db.Model):
    """Создание модели Offer"""
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    order = db.relationship("Order", foreign_keys=[order_id])
    executor = db.relationship("User", foreign_keys=[executor_id])


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
        with db.session.begin():
            db.session.add_all(new_users)


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
        with db.session.begin():
            db.session.add_all(new_orders)


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
        with db.session.begin():
            db.session.add_all(new_offers)


"""Создание и заполнение таблиц"""
db.drop_all()
db.create_all()
fulfill_users_data()
fulfill_orders_data()
fulfill_offers_data()
