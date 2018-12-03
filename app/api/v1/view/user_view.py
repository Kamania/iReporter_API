from flask import Flask, jsonify, request
from flask_restful import Resource
from app.api.v1.model import UserModel

"""Register a user"""
class Register(Resource):
    def __init__(self):
        self.user = UserModel()
    def post(self):
        data = request.get_json()

        firstname = data['firstname']
        lastname = data['lastname']
        othernames = data['othernames']
        email = data['email']
        phoneNumber = data['phoneNumber']
        username = data['username']
        registeredOn = data['registeredOn']
        isAdmin = data['isAdmin']
        password = data['password']
        password_confirmation = data['password_confirmation']
        
        if not firstname or len(firstname.strip()) == 0:
            return jsonify({"message": "First name can't be blank"}), 401
        elif not firstname or len(lastname.strip()) == 0:
            return jsonify({"message": "Last name can't be blank"}), 401
        elif not username:
            return jsonify({"message": "User name can't be left blank"}), 401
        elif not email:
            return jsonify({"message": "Email can't be left blank"}), 401
        elif not password:
            return jsonify({"message": "Password can't be left blank"}), 401
        elif password != password_confirmation:
            return jsonify({"message": "Password does not match"}), 401
        elif len(password) < 8:
            return jsonify({"message": "Password too short"}), 401

        self.user.save(id,firstname,lastname,othernames,email,phoneNumber,username,registeredOn,isAdmin,password,password_confirmation)
        return{
            "message": "successfully registered"
            }, 201

    def get(self):
        if len(self.user.get_user_data()) == 0:
            return jsonify({"message": "No user/s available now"})
        else:
            return jsonify({"data": self.user.get_user_data()})
            