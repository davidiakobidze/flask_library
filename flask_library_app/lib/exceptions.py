from flask import Blueprint, jsonify, make_response


class HandleException(Exception):
    status_code = 404

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


mod_err = Blueprint('mod_err', __name__)


@mod_err.app_errorhandler(HandleException)
def not_found_exception_handler(error):
    print(error.to_dict())
    return make_response(jsonify(error.to_dict()), error.status_code)
