from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_restful import Api

from flask_library_app.db import db
from flask_library_app.lib.exceptions import mod_err

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

from flask_library_app.resources.author import Author
from flask_library_app.resources.role import Role
from flask_library_app.resources.book import Book
from flask_library_app.resources.user import User
from flask_library_app.resources.order import Order
from flask_library_app.resources.auth import Auth

db.init_app(app)
app.register_blueprint(mod_err)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


api.add_resource(User, '/user')
api.add_resource(Role, '/role')
api.add_resource(Author, '/author')
api.add_resource(Book, '/book')
api.add_resource(Order, '/order')
api.add_resource(Auth, '/login')
