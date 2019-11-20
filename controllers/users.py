from flask_restful import Resource, request
from models.models import User
from extensions import db
from serializers.users import users_schema, user_schema


class UserListController(Resource):
    
    def get(self):
        users = User.query.all()
        return {"data": users_schema.dump(users), "message": "exito"}

    def post(self):
        data = {
            "username": request.json['username'],
            "email": request.json['email']
        }
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return {'data': user_schema.dump(new_user)}


class UserController(Resource):

    def get(self, pk):
        user = User.query.get(pk)
        if not user:
            return {"Mensaje":"No se encontro el usuario"}, 404
        single_user = []
        single_user.append(user.to_json())
        return {'usuario':user_schema.dump(user)}
        

    def put(self, pk):
        user = User.query.get(pk)
        if not user:
            return {"mensaje":"No se encontro el usuario"}, 404
        data = {
           "username": request.json['username'],
            "email": request.json['email']
        }
        user.email = data["email"]
        user.username = data["username"]
        db.session.add(user)
        db.session.commit()
        return {"usuario": user_schema.dump(user),"mensaje":"actualizado"}

    def delete(self,pk):
            user = User.query.get(pk)
            if not user:
                return {"mensaje":"No se encontro el usuario"}
            db.session.delete(user)
            db.session.commit()
            return {"usuario": user_schema.dump(user),"mensaje":"Eliminado"}

    

