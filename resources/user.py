import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type = str,
        required = True,
        help="Username cannot be left Empty!"
    )
        
    parser.add_argument('password',
        type = str,
        required = True,
        help= "Password cannot be left Empty!"
    )
        
    def post(self):
        data = UserRegister.parser.parse_args() #this line -- to send data

        if UserModel.find_by_username(data['username']):
            return {"message" : "User with the username already exists."} 

        user = UserModel(**data)    # data['name'], data['password'] = **data
        user.save_to_db()

        return {"message" : "User created Succesfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            {'message' : 'user not found'}, 404
        return user.json()

    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user :
            user.delete_from_db()
            return {'message' : 'user deleted'}, 200
        else:
            return {'message' : 'user doesnt exists'}, 404