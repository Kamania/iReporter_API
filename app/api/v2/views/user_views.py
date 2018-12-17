from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from app.api.v2.models.user_models import UserModel
import json
import re

"""Register a user"""


class Register(Resource):    

    def __init__(self):
        self.user = UserModel()
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('firstname', type=str, required=True,
                                 help='firstname is missing')
        self.parser.add_argument('lastname', type=str, required=True,
                                 help='lastname is missing')
        self.parser.add_argument('othernames', type=str, required=True,
                                 help='othernames is missing')
        self.parser.add_argument('email', type=str, required=True,
                                 help='email is missing')
        self.parser.add_argument('phoneNumber', type=str, required=True,
                                 help='phoneNumber is missing')
        self.parser.add_argument('username', type=str, required=True,
                            help='username is missing')
        self.parser.add_argument('password', type=str, required=True,
                                help='password is missing')

    def post(self):

        data = self.parser.parse_args()
        firstname = data['firstname']
        lastname = data['lastname']
        othernames = data['othernames']
        email = data['email']
        phoneNumber = data['phoneNumber']
        username = data['username']
        password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)

        user = self.user.get_user(username)
        user_email = self.user.get_email(email)

        if not firstname or len(firstname.strip()) == 0:
            return {
                'status': 401,
                'message': 'First name can\'t be blank'
                }, 401
        elif not lastname or len(lastname.strip()) == 0:
            return {
                'status': 401,
                'message': 'Last name can\'t be blank'
                }, 401
        elif not othernames or len(othernames.strip()) == 0:
            return {
                'status': 401,
                'message': 'Other name can\'t be blank'
                }, 401
        elif not username:
            return {
                'status': 401,
                'message': 'User name can\'t be left blank'
                }
        elif not email:
            return {
                'status': 401,
                'message': 'Email can\'t be left blank'
                }

        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return {'message': 'invalid email'}
            
        elif not password:
            return {'message': 'Password can\'t be left blank'}

        else:
            if user:
                return {
                    'messege': 'user with such username already exists'
                }
            if user_email:
                return {
                    'message': 'user with that email exists'
                }
            token = create_access_token(identity=email)
            self.user.save(firstname, lastname, othernames, email, phoneNumber, username, password)
            token = create_access_token(identity=email)
            del data['password']
            return {
                'status': 201,                
                'data': {
                    'token': token,
                    'user': data
                }
            }, 201

        return {
            'status': 404,
            'error': 'not successfully registered'
        }, 404

