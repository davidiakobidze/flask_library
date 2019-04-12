from werkzeug.security import safe_str_cmp

from flask_library_app.models.user import UserModel


def authenticate(user_name, password):
    print('--------')
    user = UserModel.find_by_username(user_name)
    if user and safe_str_cmp(user.password, password):
        user.id = user.user_id
        user.role = "genadi"
        print(user.user_name)
        print(user.id)
        print(user.role)
        return user


def identity(payload):
    print('++++++++')
    user_id = payload['identity']
    return UserModel.find_by_user_id(user_id)
