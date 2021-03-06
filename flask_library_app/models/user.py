from flask import jsonify

from flask_library_app import ma, bcrypt, app
from flask_library_app.db import db
from flask_library_app.lib.exceptions import HandleException


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_name = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)

    orders = db.relationship("OrderModel", backref="user", lazy=True)

    def __init__(self, first_name, last_name, user_name, password, role_id):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.role_id = role_id

    def json(self):
        user_schema = UserSchema()
        output = user_schema.dump(self).data

        return jsonify({"user": output})

    @classmethod
    def find_by_username(cls, user_name):
        user = cls.query.filter_by(user_name=user_name).first()
        return user

    @classmethod
    def find_by_user_id(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if not user:
            raise HandleException("Could not find user", 404)
        return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
