from flask import Blueprint
from flask_restful import Api, Resource
from controllers.users import UserListController, UserController

blueprint_urls = Blueprint('url_global', __name__)
api = Api(blueprint_urls, prefix='/api/web')
print("Un codigo nuevo")
api.add_resource(UserListController, "/users")
api.add_resource(UserController,"/user/<int:pk>")

