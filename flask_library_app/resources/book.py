from flask_restful import Resource, reqparse

from flask_library_app.db import db
from flask_library_app.models.book import BookModel
from flask_library_app.resources.author import AuthorModel


class Book(Resource):
    parser = reqparse.RequestParser()
    parser_authors = reqparse.RequestParser()

    parser.add_argument('isbn',
                        type=str,
                        required=True,
                        help="isbn is required")

    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="title is required")

    parser.add_argument('language',
                        type=str,
                        required=True,
                        help="language is required")

    parser.add_argument('length',
                        type=int,
                        required=True,
                        help="length is required")

    parser.add_argument('genre',
                        type=str,
                        required=True,
                        help="genre is required")

    parser_authors.add_argument('authors',
                                type=int,
                                required=True,
                                action='append',
                                help="author is required")

    def get(self):
        data = Book.parser.parse_args()
        book_id = Book.pars_search(data)
        return BookModel.find_by_id_get(book_id)

    def post(self):
        data = Book.parser.parse_args()
        parser_authors = Book.parser_authors.parse_args()
        authors_ids = parser_authors['authors']
        print(data, '-----------------')
        book = BookModel(**data)
        for authors_id in authors_ids:
            author = AuthorModel.find_by_id(authors_id)
            book.authors.append(author)
            db.session.add(book)
        db.session.commit()

        return {"message": "Book add successfully"}, 201

    def put(self):
        pass

    def delete(self):
        pass

    @classmethod
    def pars_search(cls, data):
        book_id = data['book_id']
        return BookModel.find_by_id(book_id)
