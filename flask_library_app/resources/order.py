from flask_restful import Resource, reqparse

from flask_library_app.db import db
from flask_library_app.models.book import BookModel
from flask_library_app.models.order import OrderModel
from flask_library_app.resources.auth import Auth


class Order(Resource):
    order_parser = reqparse.RequestParser()
    book_parser = reqparse.RequestParser()

    order_parser.add_argument('order_id',
                              type=int,
                              help='order id is required'
                              )

    order_parser.add_argument('price',
                              type=float,
                              help='price is required'
                              )

    order_parser.add_argument('total_price',
                              type=float,
                              help='total price is required'
                              )

    order_parser.add_argument('shipping_data',
                              type=str,
                              help='shipping data is required'
                              )

    order_parser.add_argument('user_id',
                              type=int,
                              help='user is required'
                              )

    book_parser.add_argument('books_ids',
                             type=int,
                             action='append',
                             help='books is required'
                             )

    @Auth.buyer_required
    def post(self):
        order_data = Order.order_parser.parse_args()
        book_data = Order.book_parser.parse_args()
        books_ids = book_data['books_ids']
        order = OrderModel(**order_data)

        for book_id in books_ids:
            book = BookModel.find_by_id_get(book_id)
            order.books.append(book)
            db.session.add(order)
        db.session.commit()

    @Auth.buyer_required
    def get(self):
        data = Order.order_parser.parse_args()

        order = OrderModel.find_order_by_id(data['order_id'])
        return order.json()

    @Auth.buyer_required
    def put(self):
        pass

    @Auth.buyer_required
    def delete(self):
        pass
