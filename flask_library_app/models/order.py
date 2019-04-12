import time

from flask import jsonify

from flask_library_app import ma
from flask_library_app.db import db
from flask_library_app.lib.exceptions import HandleException
from flask_library_app.models.book import BookModel

order_books = db.Table(
    "order_books",
    db.Column('book_id', db.Integer, db.ForeignKey('books.book_id')),
    db.Column('order_id', db.Integer, db.ForeignKey('orders.order_id'))
)


class OrderModel(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    total_price = db.Column(db.Float)
    shipping_data = db.Column(db.String(255))
    order_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    books = db.relationship('BookModel', secondary=order_books)

    def __init__(self, price, total_price, shipping_data, user_id):
        self.price = price
        self.total_price = total_price
        self.shipping_data = shipping_data
        self.order_date = time.strftime("%d/%m/%Y")
        self.user_id = user_id

    def json(self):
        order_schema = OrderSchema()
        output = order_schema.dump(self).data
        print(output)

        return jsonify({"order": output})

    @classmethod
    def find_order_by_id(cls, order_id):
        order = cls.query.filter_by(order_id=order_id).first()
        if not order:
            raise HandleException("cold not find order", status_code=404)
        return order


class OrderSchema(ma.Schema):
    class Meta:
        model = OrderModel


class BookSchema(ma.Schema):
    class Meta:
        table = BookModel.__table__
