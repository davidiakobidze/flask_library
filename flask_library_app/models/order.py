from db import db


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)
    books = db.relationship('BookModel', backref='order', lazy=True)
    price = db.Column(db.Float)
    total_price = db.Column(db.Float)
    shipping_data = db.Column(db.String(255))
    order_data = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
