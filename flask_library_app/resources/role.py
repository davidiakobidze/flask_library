from flask_restful import Resource, reqparse

from flask_library_app.models.role import RoleModel


class Role(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='role name is required'
                        )

    def get(self):
        return {"roles": [x.json() for x in RoleModel.query.all()]}

    def post(self):
        data = Role.parser.parse_args()
        name = data['name']

        role = RoleModel.find_by_name(name)
        if role is None:
            role = RoleModel(**data)
            role.add_to_db()
            return {"message": "role {} add successfully".format(name)}, 201
        return {"message": "role with name {} already exists".format(name)}, 409

    def put(self):
        Role.parser.add_argument('old_name', type=str)
        data = Role.parser.parse_args()
        new_name = data['name']
        old_name = data['old_name']

        role = RoleModel.find_by_name(old_name)
        if role:
            role.name = new_name
            role.add_to_db()
            return {"message": "role update successfully"}
        return {"message": "cold not find role with {} name".format(old_name)}, 404

    def delete(self):
        data = Role.parser.parse_args()
        name = data['name']

        role = RoleModel.find_by_name(name)
        if role:
            role.delete_role()
            return {"message": "role with name {} successfully delete from database".format(name)}
        return {"message": "cold not find role with name {}".format(name)}, 404
