import json
import sqlite3

import datas
from flask import request, jsonify

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


con = sqlite3.connect('New_database.db')


app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:////new_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String)


    def users_dict(self):
      return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def order_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def offer_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }

db.create_all()

for data_user in datas.users:
    raw_user = User(
        id = data_user["id"],
        first_name = data_user["first_name"],
        last_name = data_user ["last_name"],
        age = data_user ["age"],
        email = data_user ["email"],
        role = data_user ["role"],
        phone = data_user ["phone"]
    )

    db.session.add(raw_user)
    db.session.commit()

for data_order in datas.orders:
    raw_order = Order(
        id = data_order["id"],
        name = data_order["name"],
        description = data_order ["description"],
        start_date = data_order ["start_date"],
        end_date = data_order ["end_date"],
        address = data_order ["address"],
        price = data_order ["price"],
        customer_id  = data_order["customer_id"],
        executor_id = data_order["executor_id"]
    )
    db.session.add(raw_order)
    db.session.commit()

for data_offer in datas.offers:
    raw_offer = Offer(
        id = data_offer["id"],
        order_id = data_offer["order_id"],
        executor_id = data_offer["executor_id"]
    )
    db.session.add(raw_offer)
    db.session.commit()


"""Представление для пользователей, заказчиков и предложений"""


@app.route("/users", methods=['GET', 'POST'])
def get_all_users():
    """Получение всех пользователей, создание пользователя"""
    if request.method == "GET":
        users_res = []
        for i in User.query.all():
            users_res.append(i.users_dict())
        return jsonify(users_res)
    elif request.method == "POST":
        data_user = request.json
        raw_user = User(
            first_name = data_user["first_name"],
            last_name = data_user ["last_name"],
            age = data_user ["age"],
            email = data_user ["email"],
            role = data_user ["role"],
            phone = data_user ["phone"]
        )
        db.session.add(raw_user)
        db.session.commit()
        return jsonify(raw_user)

@app.route("/users/<int:x>", methods=['GET', 'DELETE', 'POST'])
def get_one_user(x):
    """Получения одного пользователя, обновление пользователя, удаление пользователя"""
    if request.method == "GET":
        return jsonify(User.query.get(x).users_dict())
    elif request.method == "DELETE":
        i = User.query.get(x)
        db.session.delete(i)
        db.session.commit()
        return jsonify(i)
    elif request.method == "PUT":
        data_user = request.json
        i = User.query.get(x)
        i.first_name = data_user["first_name"],
        i.last_name = data_user ["last_name"],
        i.age = data_user ["age"],
        i.email = data_user ["email"],
        i.role = data_user ["role"],
        i.phone = data_user ["phone"]
        db.session.add(i)
        db.session.commit()
        return jsonify(i)


@app.route("/orders", methods=['GET', 'POST'])
def get_all_orders():
    """Получение всех заказчиков, создание заказчика"""
    if request.method == "GET":
        orders_res = []
        for i in Order.query.all():
            orders_res.append(i.order_dict())
        return jsonify(orders_res)
    elif request.method == "POST":
        data_order = request.json
        raw_order = Order(
            name=data_order["name"],
            description=data_order["description"],
            start_date=data_order["start_date"],
            end_date=data_order["end_date"],
            address=data_order["address"],
            price=data_order["price"],
            customer_id=data_order["customer_id"],
            executor_id=data_order["executor_id"]
        )
        db.session.add(raw_order)
        db.session.commit()
        return jsonify(raw_order)

@app.route("/orders/<int:x>", methods=['GET', 'POST', 'DELETE'])
def get_one_order(x):
    """Получения одного заказчика, обновление заказчика, удаление заказчика"""
    if request.method == "GET":
        return jsonify(Order.query.get(x).order_dict())
    elif request.method == "DELETE":
        i = Order.query.get(x)
        db.session.delete(i)
        db.session.commit()
        return json.dumps(i)
    elif request.method == "PUT":
        data_order = request.json
        i = Order.query.get(x)
        i.name=data_order["name"],
        i.description = data_order["description"],
        i.start_date = data_order["start_date"],
        i.end_date = data_order["end_date"],
        i.address = data_order["address"],
        i.price = data_order["price"],
        i.customer_id = data_order["customer_id"],
        i.executor_id = data_order["executor_id"]
        db.session.add(i)
        db.session.commit()
        return jsonify(i)

@app.route("/offers", methods=['GET', 'POST'])
def get_all_offers():
    """Получение всех предложений, создание предложения"""
    if request.method == "GET":
        offers_res = []
        for i in Offer.query.all():
            offers_res.append(i.offer_dict())
        return jsonify(offers_res)
    elif request.method == "POST":
        data_offer = request.json
        raw_offer = Offer(
            order_id=data_offer["order_id"],
            executor_id=data_offer["executor_id"]
        )
        db.session.add(raw_offer)
        db.session.commit()
        return jsonify(raw_order)

@app.route("/offers/<int:x>", methods=['GET', 'POST', 'DELETE'])
def get_one_offer(x):
    """Получения одного предложения, обновление предложения, удаление предложения"""
    if request.method == "GET":
        return jsonify(Offer.query.get(x).offer_dict())
    elif request.method == "DELETE":
        i = Offer.query.get(x)
        db.session.delete(i)
        db.session.commit()
        return jsonify(i)
    elif request.method == "PUT":
        data_offer = request.json
        i = Offer.query.get(x)
        i.order_id = data_offer["order_id"],
        i.executor_id = data_offer["executor_id"]
        i.db.session.add(i)
        i.db.session.commit()
        return jsonify(i)

if __name__ == "__main__":
    app.run()