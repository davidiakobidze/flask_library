from flask_library_app.db import db
from flask_library_app.lib.exceptions import HandleException


class AuthorModel(db.Model):
    __tablename__ = "authors"

    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    age = db.Column(db.Integer())
    nationality = db.Column(db.String(25))

    def __init__(self, first_name, last_name, age, nationality):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.nationality = nationality

    def json(self):
        return {
            "first name": self.first_name,
            "last name": self.last_name,
            "age": self.age,
            "nationality": self.nationality
        }

    @classmethod
    def find_by_name(cls, first_name, last_name):
        return cls.query.filter_by(first_name=first_name, last_name=last_name).first()

    @classmethod
    def find_by_id(cls, author_id):
        author = cls.query.filter_by(author_id=author_id).first()
        if not author:
            raise HandleException("Could not find author with id {}".format(author_id), 404)
        return author

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
