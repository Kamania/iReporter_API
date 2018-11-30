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
        data = request.get_json()['name']

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
            "message": "Record saved successful"
        }, 201
        # return resp, 201
        # return jsonify({"message": "Record added successfull"},201)

    """The method gets all the records"""
    def get(self):
        return self.details.get_redFlag(), 200
        # return{
        #     "message": "Successfully viewed"
        # }, 200

"""The class posts and gets a specific record"""
class UserReportRedFlag(Resource, RaiseRedFlagModel):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Get specific record"""
    def get(self, id):
        return self.details.find(id), 200

    """Edit specific record"""
    def patch(self, id):
        data = request.get_json()
        record_id = self.details.find(id)

        if not record_id:
            return jsonify({"message": "record not found"},200)
        record_update = record_id.update(data), 200
        return jsonify({
            "message": "record updated",
            "data": record_update[id]
        })

    """Deletes a specific record"""
    def delete(self, id):
        record_id = self.details.find(id)
        del_record = self.details.get_redFlag()

        if record_id != 0:
            return del_record.pop(record_id), 200
        return jsonify({"message": "record not found","status": "404"}),404