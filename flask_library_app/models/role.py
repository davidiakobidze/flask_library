from flask_library_app.db import db


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

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {"name": self.name}

    def delete_role(self):
        db.session.delete(self)
        db.session.commit()
