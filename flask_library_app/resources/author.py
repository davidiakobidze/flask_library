from flask_restful import Resource, reqparse

from flask_library_app.models.author import AuthorModel


class Author(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="first name is required"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="last name is required"
                        )
    parser.add_argument('age',
                        type=int,
                        required=True,
                        help="age is required"
                        )
    parser.add_argument('nationality',
                        type=str,
                        required=True,
                        help="nationality is required"
                        )

    def get(self):
        return {"Authors": [x.json() for x in AuthorModel.query.all()]}

    def post(self):
        data = Author.parser.parse_args()
        author = Author.pars_search(data)
        if author:
            return {"message": "author {} {} already exists".format(data['first_name'], data['last_name'])}, 409
        author = AuthorModel(**data)
        author.add_to_db()
        return {"message": "successfully add author {} {}".format(data['first_name'], data['last_name'])}, 201

    def put(self):
        data = Author.parser.parse_args()
        author = Author.pars_search(data)
        if author is None:
            return {"message": "Cold not find author"}, 404
        author.first_name = data['first_name']
        author.last_name = data['last_name']
        author.age = data['age']
        author.nationality = data['nationality']
        author.add_to_db()
        return {"message": "Author updated successfully"}

    def delete(self):
        data = Author.parser.parse_args()
        author = Author.pars_search(data)
        if author is None:
            return {"message": "Cold not find author"}, 404
        author.delete_from_db()
        return {
            "message": "Successfully delete author with name {} {}".format(data['firs_name'], data['last_name'])
        }

    @classmethod
    def pars_search(cls, data):
        first_name = data['first_name']
        last_name = data['last_name']
        return AuthorModel.find_by_name(first_name, last_name)
