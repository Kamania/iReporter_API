from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from app.api.v2.models.record_models import RaiseRedFlagModel
import json
import re

parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('type',
                    choices=('Red-Flag', 'Intervention', 'redflag', 'intervention', 'red-flag'),
                    help="Bad choice: {error_msg}"
                    )

parser.add_argument("location", type=str, required=True,
                    help="location is missing")

parser.add_argument('status',
                    choices=('Rejected', 'Resolved',
                             'Not yet resolved', 'Draft'),
                    help="Bad choice: {error_msg}"
                    )

parser.add_argument("comments", type=str, required=True,
                    help="Comment item is missing")


"""The class posts all records"""


class UserReportRedFlagList(Resource):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    @jwt_required
    def post(self):
        """
        It checks for the most important fields which
        should not be left blank and returns "Record Added Successful"
        """

        args = parser.parse_args()
        data = request.get_json()
        user = get_jwt_identity()
        user_id = user.get('user_id')

        ci_type = data['type']
        location = data['location']
        status = data['status']
        comments = data['comments']

        if not location or len(location.split()) == 0:
            return {
                'status': 400,
                'message': 'Location cannot be left blank'
                }, 400

        elif not ci_type or len(ci_type.split()) == 0:
            return {
                'status': 400,
                'message': 'Record type cannot be left blank'
                }, 400

        elif not re.match(r"^([-+]?\d{1,2}([.]\d+)?),\s*([-+]?\d{1,3}([.]\d+)?)$", location):
            return {
                'status': 400,
                'message': 'Please ensure to seperate lat and long with a\
                 comma, lat and long are numbers, lat and long are within\
                 their appropriate range.'
                }, 400

        elif not status or len(status.split()) == 0:
            return {
                'status': 400,
                'message': 'Status cannot be left blank'
                }, 400

        elif re.match(r"([@_!#$%^&*()<>?/\|}{~:])", comments):
            return {
                'status': 401,
                'message': 'Comment cannot contain special characters'
                }, 401

        elif not comments or len(comments.split()) == 0:
            return {
                'status': 400,
                'message': 'Comments cannot be left blank'
                }, 400
        
        self.details.save(user_id, ci_type, location, status, comments)

        return {
            'status': 201,
            'data': [{
                'data': data
            }]
        }, 201

    """The method gets all the records"""
    @jwt_required
    def get(self):
        current_user = get_jwt_identity().get('user_id')
        user = current_user
        get_all = self.details.get_redFlag(user)
        get_all = self.details.check_record(get_all)

        if not get_all and len(get_all) == 0:
            return {
                'status': 404,
                'message': 'No record(s) found'
            }, 404
        return {
            'status': 200,
            'data': get_all
        }, 200

 
"""The class posts and gets a specific record"""


class UserReportRedFlag(Resource, RaiseRedFlagModel):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Get specific record"""
    @jwt_required
    def get(self, id):
        current_user = get_jwt_identity().get('user_id')
        user = current_user
        get_specific = self.details.find(int(id), user)
    
        if not get_specific:
            return {
                'status': 404,
                'message': 'record not found'
            }, 404
        get_specific = self.details.check_record(get_specific)
        return {
            'status': 200,
            'data': get_specific
        }, 200
        check_record(record)

    
    """Deletes a specific record"""

    @jwt_required
    def delete(self, id):        
        record = self.details.get_record_by_id(id)
        current_user = get_jwt_identity().get('user_id')
        if not record:
            return {
                'status': 404,
                'error': 'record not found'
            }, 404
        
        created_by = record['createdby']
        if current_user != created_by:
            return {
                'status': 403,
                'error': 'cannot delete other user\'s data'
            }, 403
        record = self.details.del_record(id)
        return {
            'status': 200,
            'message': 'successfully deleted record'
        }, 200              


class Patch_location(Resource, RaiseRedFlagModel):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Edit specific record"""
    @jwt_required
    def patch(self, id):
        data = parser.parse_args()
        current_user = get_jwt_identity().get('user_id')
        location = data['location']
        record = self.details.get_record_by_id(id)

        if re.match(r"([@_!#$%^&*()<>?/\|}{~:])", data['location']):
            return {'message': 'location should not contain special characters'}

        if not data['location'] or len(data['location'].split()) == 0:
            return {
                'status': 400,
                'message': 'Location cannot be left blank'
                }, 400

        if not record:
            return {
                'status': 404,
                'error': 'record not found'
            }, 404

        created_by = record['createdby']
        if current_user != created_by:
            return {
                'status': 403,
                'error': 'cannot edit other user\'s data'
            }, 403
        self.details.update_location(location, id)
        return {
            'status': 200,
            'message': 'Succesfully updated location'
        }, 200


class Patch_comment(Resource, RaiseRedFlagModel):

    """Edit specific record"""
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Edit specific record"""
    @jwt_required
    def patch(self, id):
        data = parser.parse_args()
        current_user = get_jwt_identity().get('user_id')
        comment = data['comments']
        record = self.details.get_record_by_id(id)

        if re.match(r"([@_!#$%^&*()<>?/\|}{~:])", data['comments']):
            return {'message': 'comment should not contain special characters'}

        if not data['comments'] or len(data['comments'].split()) == 0:
            return {
                'status': 400,
                'message': 'comments cannot be left blank'
                }, 400
        if not record:
            return {
                'status': 500,
                'message': 'comments not updated'
            }, 500

        created_by = record['createdby']
        if current_user != created_by:
            return {
                'status': 403,
                'error': 'cannot edit other user\'s data'
            }, 403
        self.details.update_comment(comment, id)
        return {
            'status': 200,
            'message': 'Succesfully updated comments'
        }, 200


class Patch_status(Resource, RaiseRedFlagModel):

    """Edit specific record"""
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Edit specific record"""
    @jwt_required
    def patch(self, id):
        data = parser.parse_args()
        record = self.details.get_record_by_id(id)
        current_user = get_jwt_identity().get('user_id')
        admin = self.details.check_isAdmin(str(current_user))
        status = data['status']
        
        if re.match(r"([@_!#$%^&*()<>?/\|}{~:])", data['comments']):
            return {'message': 'comment should not contain special characters'}

        if not data['comments'] or len(data['comments'].split()) == 0:
            return {
                'status': 400,
                'message': 'comments cannot be left blank'
                }, 400
        if not record:
            return {
                'status': 500,
                'message': 'comments not updated'
            }, 500
        if not admin:
            return {
                'status': 403,
                'error': 'You are not allowed to update'
            }, 403

        self.details.update_status(status, id)
        return {
            'status': 200,
            'message': 'Succesfully updated status'
        }, 200
