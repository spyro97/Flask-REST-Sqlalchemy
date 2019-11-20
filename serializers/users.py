from marshmallow import Schema


class UserSchema(Schema):

    class Meta:
        fields = ('id', 'username', 'email')
        ordered = True


users_schema = UserSchema(many=True)
user_schema = UserSchema()
