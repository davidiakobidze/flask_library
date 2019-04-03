from flask_restful import Resource, reqparse


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
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
