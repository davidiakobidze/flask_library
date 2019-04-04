from flask_restful import Resource, reqparse

from flask_library_app.models.book import BookModel


class Book(Resource):
    parser = reqparse.RequestParser()

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

    def get(self):
        data = Book.parser.parse_args()
        book = Book.pars_search(data)
        if book is None:
            return {"message": "Could not find book"}
        return

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    @classmethod
    def pars_search(cls, data):
        book_id = data['book_id']
        return BookModel.find_by_id(book_id)
