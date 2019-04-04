from flask_library_app.db import db

book_authors = db.Table(
    'books_authors',
    db.Column('author_id', db.Integer, db.ForeignKey('authors.author_id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.book_id'))
)


class BookModel(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(16))
    title = db.Column(db.String(80))
    language = db.Column(db.String(80))
    length = db.Column(db.Integer)
    genre = db.Column(db.String(80))

    authors = db.relationship('AuthorModel', secondary=book_authors)

    def __init__(self, isbn, title, language, length, genre):
        self.isbn = isbn
        self.title = title
        self.language = language
        self.length = length
        self.genre = genre

    @classmethod
    def find_by_id(cls, book_id):
        return cls.query.filter_by(book_id=book_id).first()

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_book(self):
        db.session.delete(self)
        db.session.commit()
