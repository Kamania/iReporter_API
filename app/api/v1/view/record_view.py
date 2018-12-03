from flask_restful import Resource
from flask import jsonify, request, make_response
from app.api.v1.model import RaiseRedFlagModel
import json

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
        
        self.details.save(id, createdOn, createdBy, ci_type, location, status, photo, video, comments)
        return{
            "status": 201,          
            "data":{
                "id": len(self.details.get_redFlag()),
                "message": "Created record successfully"
            }                  
        }, 201

    """The method gets all the records"""
    def get(self):
        get_all = self.details.get_redFlag()
        return{
            "status": 200,
            "data": get_all
        }, 200

"""The class posts and gets a specific record"""
class UserReportRedFlag(Resource, RaiseRedFlagModel):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Get specific record"""
    def get(self, id):
        get_specific = self.details.find(id)
        return{
            "status":200,
            "data": get_specific
        },200

    """Edit specific record"""
    def patch(self, id):
        data = request.get_json()
        record_id = self.details.find(id)

        if not record_id:
            return jsonify({"message": "record not found"},200)
        record_update = record_id.update(data)
        return jsonify({
            "id": record_update[id],
            "message": "record updated"            
        }),200

    """Deletes a specific record"""
    def delete(self, id):
        record = self.details.find(id)

        if not record:
            return {"status": 404, "message": "record not found"}, 404 
        
        self.details.get_redFlag().remove(record)

        return {
                "status": 200,
                "data": [{
                    "id": len(self.details.get_redFlag())+1,
                    'message': 'successfully deleted record'
                }]
        }, 200 