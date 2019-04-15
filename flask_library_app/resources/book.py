from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from flask_library_app.db import db
from flask_library_app.models.book import BookModel
from flask_library_app.resources.auth import Auth
from flask_library_app.resources.author import AuthorModel


class Book(Resource):
    parser = reqparse.RequestParser()
    book_id_parser = reqparse.RequestParser()
    parser_authors = reqparse.RequestParser()

    book_id_parser.add_argument('book_id',
                                type=int,
                                required=True,
                                help="book id is required is required")

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

    @jwt_required
    def get(self):
        data = Book.parser.parse_args()
        book_id = Book.pars_search(data)
        return BookModel.find_by_id_get(book_id)

    @Auth.admin_required
    def post(self):
        data = Book.parser.parse_args()
        parser_authors = Book.parser_authors.parse_args()
        authors_ids = parser_authors['authors']
        book = BookModel(**data)
        for authors_id in authors_ids:
            author = AuthorModel.find_by_id(authors_id)
            book.authors.append(author)
            db.session.add(book)
        db.session.commit()

        return {"message": "Book add successfully"}, 201

    # @Auth.admin_required
    # def put(self):
    #     data = Book.parser.parse_args()
    #     author_data = Book.parser_authors.parse_args()
    #     book_id = Book.book_id_parser.parse_args()['book_id']
    #     book = BookModel.find_by_id_get(book_id)
    #     book.isbn = data["isbn"]
    #     book.title = data["title"]
    #     book.language = data["language"]
    #     book.length = data["length"]
    #     book.genre = data["genre"]
    #     print(author_data)
    #     book.authors = author_data['authors']
    #     book.add_to_db()
    #     return {"message": "Book update successfully"}

    @Auth.admin_required
    def delete(self):
        book_id = Book.parser.parse_args()['book_id']
        book = BookModel.find_by_id_get(book_id)
        book.delete_book()
        return {"message": "Book remove successfully"}

    @classmethod
    def pars_search(cls, data):
        book_id = data['book_id']
        return BookModel.find_by_id(book_id)
