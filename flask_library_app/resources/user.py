from flask_restful import Resource, reqparse

from flask_library_app.lib.exceptions import HandleException
from flask_library_app.models.user import UserModel
from flask_library_app.resources.auth import Auth


class User(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('first_name',
                        type=str,
                        help="user first name is required"
                        )

    parser.add_argument('last_name',
                        type=str,
                        help="user last name is required"
                        )

    parser.add_argument('user_name',
                        type=str,
                        help="user user name is required"
                        )

    parser.add_argument('password',
                        type=str,
                        help="user password is required"
                        )

    parser.add_argument('role_id',
                        type=int,
                        help="user role is required"
                        )

    @Auth.admin_required
    def get(self, username):
        user = UserModel.find_by_username(username)
        if not user:
            return {"message": "could not find user with '{}' username".format(username)}, 404
        return user.json()

    def post(self):
        data = User.parser.parse_args()
        user = UserModel.find_by_username(data['user_name'])
        if user:
            raise HandleException("User already exists", status_code=409)
        user = UserModel(**data)
        print(user)
        user.save_to_db()
        return {"message": "user with name {} {} add successfully".format(data['first_name'], data['last_name'])}

    @Auth.admin_required
    def update(self):
        data = User.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user is None:
            user = UserModel(**data)
        else:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.user_name = data['user_name']
            user.role = data['role']

        user.save_to_db()
        return user.json()

    @Auth.admin_required
    def delete(self):
        data = User.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user:
            user.delete_from_db()
            return {"message": "delete successfully"}

        return {"message": "could not find user with '{}' username".format(data['username'])}, 404
