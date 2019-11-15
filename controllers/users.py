from flask_restful import Resource, request
from models.models import User
from extensions import db


class UserListController(Resource):
    
    def get(self):
        users = User.query.all()
        user_data = []
        for userr in users:
            user_data.append(userr.to_json())
        return {"data": user_data, "message": "exito"}

    def post(self):
        data = {
            "username": request.json['username'],
            "email": request.json['email']
        }
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return {'data': new_user.to_json()}


class UserController(Resource):

    def get(self, pk):
        user = User.query.get(pk)
        if not user:
            return {"Mensaje":"No se encontro el usuario"}, 404
        single_user = []
        single_user.append(user.to_json())
        return {"usuario":single_user}
        

    def put(self, pk):
        pass

    def delete(self,pk):
        pass

    

