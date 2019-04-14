from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from flask_library_app.lib.exceptions import HandleException
from flask_library_app.models.author import AuthorModel
from flask_library_app.resources.auth import Auth


class Author(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('author_id',
                        type=int,
                        help="author id is required"
                        )
    parser.add_argument('first_name',
                        type=str,
                        help="first name is required"
                        )
    parser.add_argument('last_name',
                        type=str,
                        help="last name is required"
                        )
    parser.add_argument('age',
                        type=int,
                        help="age is required"
                        )
    parser.add_argument('nationality',
                        type=str,
                        help="nationality is required"
                        )

    @jwt_required
    def get(self):
        return {"Authors": [x.json() for x in AuthorModel.query.all()]}

    @Auth.admin_required
    def post(self):
        data = Author.parser.parse_args()
        author = Author.pars_search(data)
        if author:
            raise HandleException("author {} {} already exists".format(data['first_name'], data['last_name']), 409)
        author = AuthorModel(**data)
        author.add_to_db()
        return {"message": "successfully add author {} {}".format(data['first_name'], data['last_name'])}, 201

    @Auth.admin_required
    def put(self):
        data = Author.parser.parse_args()
        author = AuthorModel.find_by_id(data['author_id'])
        author.first_name = data['first_name']
        author.last_name = data['last_name']
        author.age = data['age']
        author.nationality = data['nationality']
        author.add_to_db()
        return {"message": "Author updated successfully"}

    @Auth.admin_required
    def delete(self):
        author_id = Author.parser.parse_args()["author_id"]
        author = AuthorModel.find_by_id(author_id)
        author.delete_from_db()
        return {"message": "Successfully delete author"}

    @classmethod
    def pars_search(cls, data):
        first_name = data['first_name']
        last_name = data['last_name']
        return AuthorModel.find_by_name(first_name, last_name)
