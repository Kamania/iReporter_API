from flask_restful import Resource
from flask import jsonify, request, make_response
from .model import RaiseRedFlagModel

class UserDetails(Resource, RaiseRedFlagModel):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    def post(self):
        data = request.get_json()
        orgName = data['organization name']
        pName = data["person's name"]
        corruption_type = data['corruption type']
        other = data['other']
        description = data['other']
        photo = data['photo']
        video = data['video']
        geolocation = data['geolocation']

        resp = self.details.save(id,orgName,pName,corruption_type,other,description,photo,video,geolocation)

        return resp, 201

    def get(self):
        return self.details, 200