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
                'error': 'First name can\'t be blank'
                }, 401
        elif not lastname or len(lastname.strip()) == 0:
            return {
                'status': 401,
                'error': 'Last name can\'t be blank'
                }, 401
        elif not othernames or len(othernames.strip()) == 0:
            return {
                'status': 401,
                'error': 'Other name can\'t be blank'
                }, 401
        elif not username:
            return {
                'status': 401,
                'error': 'User name can\'t be left blank'
                }, 401
        elif not email:
            return {
                'status': 401,
                'error': 'Email can\'t be left blank'
                }, 401

        elif not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return {
                'status': 401,
                'error': 'invalid email'
                }, 401
            
        elif not password:
            return {
                'status': 401,
                'message': 'Password can\'t be left blank'
                }, 401

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


class UserLogin(Resource, UserModel):
    def __init__(self):
        self.user = UserModel()
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('username', type=str, required=True,
                                 help='username is missing')
        self.parser.add_argument('password', type=str, required=True,
                                 help='password is missing')

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        username = username.strip()
        password = password.strip()

        if not username or not password:
            return {
                'status': 400,
                'error': 'please fill in all the fields'
            }, 400
        
        user = self.user.get_user(username)
        if not user:
            return {
                'status': 404,
                'message': 'No user with such username'
            }, 404
        
        passw = user.get('password')        
        
        if not check_password_hash(passw, password):
            return {
                'status': 401,
                'message': 'Invalid password'
            }, 401

        token = create_access_token(identity=user, fresh=True)
        user['registeredon'] = user['registeredon'].strftime('%A %d. %B %Y')
        del user['password']

        return {
            'status': 200,
            'access token': token,
            'user': user
        }, 200
