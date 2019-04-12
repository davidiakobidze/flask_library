from flask_library_app.db import db
from flask_library_app.lib.exceptions import HandleException


class RoleModel(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    users = db.relationship('UserModel', backref='roles', lazy=True)

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, role_id):
        role = cls.query.filter_by(role_id=role_id).first()
        if not role:
            raise HandleException("Could not find role", 404)
        return role

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {"name": self.name}

    def delete_role(self):
        db.session.delete(self)
        db.session.commit()
