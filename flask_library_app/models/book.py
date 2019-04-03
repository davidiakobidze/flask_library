from db import db

authors = db.Table(
    'authors',
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'), primary_key=True)
)


class BookModel(db.Model):
    __tablename__ = "book"

    book_id = db.Column(db.String(80), primary_key=True)
    isbn = db.Column(db.String(16))
    title = db.Column(db.String(80))
    language = db.Column(db.String(80))
    length = db.Column(db.Integer)
    genre = db.Column(db.String(80))

    authors = db.relationship('AuthorModel', secondary=authors, lazy='subquery', backref=db.backref('books', lazy=True))

    def __init__(self, isbn, title, language, length, genre):
        self.isbn = isbn
        self.title = title
        self.language = language
        self.length = length
        self.genre = genre

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.find_by(isbn=isbn).first()

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        db.session.delete(self)
        db.session.commit()
