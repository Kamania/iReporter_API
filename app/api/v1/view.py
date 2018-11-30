from flask_restful import Resource
from flask import jsonify, request, make_response
from .model.model import RaiseRedFlagModel

"""The class posts all records"""
class UserReportRedFlagList(Resource):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    def post(self):
        """
        It checks for the most important fields which 
        should not be left blank and returns "Record Added Successful"
        """
        data = request.get_json()

        createdOn = data['createdOn']
        createdBy = data["createdBy"]
        ci_type = data['type']
        location = data['location']
        status = data['status']
        photo = data['photo']
        video = data['video']
        comments = data['comments']

        if not createdOn:
            return jsonify({"message": "Date cannot be left blank"}),
        elif not location:
            return jsonify({"message": "Location cannot be left blank"}),
        
        # resp = 
        self.details.save(id, createdOn, createdBy, ci_type, location, status, photo, video, comments)
        return{
            "id": id,
            "message": "Record saved successful"
        }, 201
        # return resp, 201
        # return jsonify({"message": "Record added successfull"},201)