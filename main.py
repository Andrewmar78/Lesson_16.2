from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import get_users_all, get_offers_all, get_orders_all
from datetime import datetime

import logging
logging.basicConfig(filename="basic.log", level=logging.INFO)


"""Запуск SQLAlchemy"""
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///configs/cache.sqlite3"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Строчка ниже не хочет работать без ошибок, пришлось записать две верхние (из интернета)
# app.config["SQLAlchemy_DATABASE_URI"] = "sqlite:///sqlite3.db"
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


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


@app.route("/users", methods=['GET', 'POST'])
def all_users_page():
    """Вьюшка страницы пользователей"""
    if request.method == "GET":
        data = []
        for user in User.query.all():
            data.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone,
            })
        return render_template("index.html", users=data)
    elif request.method == "POST":
        data = request.get_json()
        new_user = User(
                id=data["id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                age=data["age"],
                email=data["email"],
                role=data["role"],
                phone=data["phone"],
            )
        with db.session.begin():
            db.session.add(new_user)
        return "", 201


@app.route("/users/<int:user_id>", methods=['GET', 'PUT', 'DELETE'])
def users_page_by_id(user_id):
    """Вьюшка страницы одного из пользователей"""
    if request.method == "GET":
        try:
            data = {}
            user = User.query.get(user_id)
            data = {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "age": user.age,
                    "email": user.email,
                    "role": user.role,
                    "phone": user.phone,
                }
            return jsonify(data)
        except AttributeError:
            return "Пользователя с таким номером нет"

    elif request.method == "PUT":
        data = request.get_json()
        user = Order.query.get(user_id)
        # user.id = data["id"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.age = data["age"]
        user.email = data["email"]
        user.role = data["role"]
        user.phone = data["phone"]

        with db.session.begin():
            db.session.add(user)

        print(User.query.filter(User.first_name == "new_user").first().first_name)
        return "", 203

    elif request.method == "DELETE":
        user = User.query.get(user_id)

        with db.session.begin():
            db.session.delete(user)


@app.route("/orders", methods=['GET', 'POST'])
def all_orders_page():
    """Вьюшка страницы заказов"""
    if request.method == "GET":
        data = []
        for order in Order.query.all():
            data.append({
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": order.customer_id,
                "executor": order.executor,
            })
        return render_template("orders.html", orders=data)

    elif request.method == "POST":
        data = request.get_json()
        new_order = Order(
                id=data["id"],
                name=data["name"],
                description=data["description"],
                start_date=datetime.strptime(data["start_date"], '%m/%d/%Y'),
                end_date=datetime.strptime(data["end_date"], '%m/%d/%Y'),
                address=data["address"],
                price=data["price"],
                customer_id=data["customer_id"],
                executor_id=data["executor_id"],
            )
        with db.session.begin():
            db.session.add(new_order)
        return "", 201


@app.route("/orders/<int:order_id>", methods=['GET', 'PUT', 'DELETE'])
def orders_page_by_id(order_id):
    """Вьюшка страницы одного из заказов"""
    if request.method == "GET":
        try:
            data = {}
            order = Order.query.get(order_id)
            data = {
                    "id": order.id,
                    "name": order.name,
                    "description": order.description,
                    "start_date": order.start_date,
                    "end_date": order.end_date,
                    "address": order.address,
                    "price": order.price,
                    "customer_id": order.customer_id,
                    "executor_id": order.executor_id,
                }
            return jsonify(data)
        except AttributeError:
            return "Заказа с таким номером нет"

    elif request.method == "PUT":
        data = request.get_json()
        order = Order.query.get(order_id)
        # order.id = data["id"]
        order.name = data["name"]
        order.description = data["description"]
        order.start_date = datetime.strptime(data["start_date"], '%m/%d/%Y')
        order.end_date = datetime.strptime(data["end_date"], '%m/%d/%Y')
        order.address = data["address"]
        order.price = data["price"]
        order.customer_id = data["customer_id"]
        order.executor_id = data["executor_id"]

        with db.session.begin():
            db.session.add(order)

        print(Order.query.filter(Order.name == "new_order").first().name)
        return "", 203

    elif request.method == "DELETE":
        order = Order.query.get(order_id)

        with db.session.begin():
            db.session.delete(order)


@app.route("/offers", methods=['GET', 'POST'])
def all_offers_page():
    """Вьюшка страницы предложений"""
    if request.method == "GET":
        data = []
        for offer in Offer.query.all():
            data.append({
                "id": offer.id,
                "order_id": offer.order_id,
                "executor_id": offer.executor_id,
            })
        return render_template("offers.html", offers=data)
        # return jsonify(data)

    elif request.method == "POST":
        data = request.get_json()
        new_offer = Offer(
                id=data["id"],
                order_id=data["order_id"],
                executor_id=data["executor_id"],
            )
        with db.session.begin():
            db.session.add(new_offer)
        return "", 201


@app.route("/offers/<int:offer_id>", methods=['GET', 'PUT', 'DELETE'])
def offers_page_by_id(offer_id):
    """Вьюшка страницы одного из предложений"""
    if request.method == "GET":
        try:
            data = {}
            offer = Offer.query.get(offer_id)
            data = {
                    "id": offer.id,
                    "order_id": offer.order_id,
                    "executor_id": offer.executor_id,
                }
            return jsonify(data)
        except AttributeError:
            return "Предложения с таким номером нет"

    elif request.method == "PUT":
        data = request.get_json()
        offer = Offer.query.get(offer_id)
        # offer.id = data["id"]
        offer.order_id = data["order_id"]
        offer.executor_id = data["executor_id"]

        with db.session.begin():
            db.session.add(offer)

        print(Offer.query.filter(Offer.id == "1000").first().id)
        return "", 203

    elif request.method == "DELETE":
        offer = Offer.query.get(offer_id)

        with db.session.begin():
            db.session.delete(offer)


@app.route("/api/users")
def get_all_users_json():
    """API для возврата всех пользователей в JSON"""
    data = get_users_all()
    return jsonify(data)

# Проверки
# get_users_all()
# get_orders_all()
# get_offers_all()

# fulfill_users_data()
# fulfill_orders_data()
# fulfill_offers_data()
#
# print(User.query.get(1).first_name)
# print(Order.query.get(1).name)
# print(Offer.query.get(1).order_id)

if __name__ == '__main__':
    app.run(debug=True)
