from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import (
    verify_jwt_in_request,
    create_access_token,
    get_jwt_identity
)
from flask_restful import Resource

from flask_library_app import bcrypt
from flask_library_app.models.role import RoleModel
from flask_library_app.models.user import UserModel


class Auth(Resource):

    def post(self):
        user_name = request.json.get('username')
        password = request.json.get('password')
        user = UserModel.find_by_username(user_name)
        if not user or not bcrypt.check_password_hash(
                user.password, password
        ):
            return {"message": "Bad username or password"}, 401
        user_object = {"user_name": user.user_name, "roles": user.role_id}
        access_token = create_access_token(identity=user_object)
        ret = {'access_token': access_token}
        return ret, 200

    def admin_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            role = RoleModel.find_by_id(identity['roles'])
            if role.name != 'admin':
                return jsonify(msg='You have not right'), 403
            else:
                return fn(*args, **kwargs)

        return wrapper

    def buyer_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            role = RoleModel.find_by_id(identity['roles'])
            if role.name != 'buyer':
                return jsonify(msg='You have not right'), 403
            else:
                return fn(*args, **kwargs)

        return wrapper
