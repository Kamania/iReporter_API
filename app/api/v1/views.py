from flask import Flask, jsonify, request
from flask_restful import Resource, reqparse
from app.api.v1.models import UserModel, RaiseRedFlagModel
import json
import re

parser = reqparse.RequestParser(bundle_errors=True)

parser.add_argument('createdOn', type=str, required=True,
                    help='createdOn is missing')

parser.add_argument('createdBy', type=str, required=True,
                    help='createdBy is missing')

parser.add_argument('type',
                    choices=('Red-Flag', 'Incidence'),
                    help="Bad choice: {error_msg}"
                    )

parser.add_argument("location", type=str, required=True,
                    help="location is missing")

parser.add_argument('status',
                    choices=('Rejected', 'Resolved',
                             'Not yet resolved', 'Draft'),
                    help="Bad choice: {error_msg}"
                    )

parser.add_argument("photo", type=str, required=True,
                    help="photo item is missing")

parser.add_argument("video", type=str, required=True,
                    help="video item is missing")

parser.add_argument("comments", type=str, required=True,
                    help="Comment item is missing")


"""The class posts all records"""


class UserReportRedFlagList(Resource):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    def post(self):
        """
        It checks for the most important fields which
        should not be left blank and returns "Record Added Successful"
        """

        args = parser.parse_args()
        data = request.get_json()

        createdOn = data['createdOn']
        createdBy = data['createdBy']
        ci_type = data['type']
        location = data['location']
        status = data['status']
        photo = data['photo']
        video = data['video']
        comments = data['comments']

        if re.match(r"([@_!#$%^&*()<>?/\|}{~:])", createdOn):
            return {'message': 'Invalid date'}

        elif not createdOn or len(createdOn.split()) == 0:
            return {'message': 'Date cannot be left blank'}

        elif re.match(r"([@_!#$%^&*()<>?/\|}{~:])", createdBy):
            return {'message': 'Invalid name'}

        elif not createdBy or len(createdBy.split()) == 0:
            return {'message': 'Reporter cannot be left blank'}

        elif not ci_type or len(ci_type.split()) == 0:
            return {'message': 'Record type cannot be left blank'}

        elif re.match(r"([@_!#$%^&*()<>?/\|}{~:])", location):
            return {'message': 'Invalid location'}

        elif not location or len(location.split()) == 0:
            return {'message': 'Location cannot be left blank'}

        elif not status or len(status.split()) == 0:
            return {'message': 'Status cannot be left blank'}

        elif re.match(r"([@_!#$%^&*()<>?/\|}{~:])", comments):
            return {'message': 'Comment cannot contain special characters'}

        elif not comments or len(comments.split()) == 0:
            return {'message': 'Comments cannot be left blank'}

        elif self.details.save(id, createdOn, createdBy, ci_type, location,
                               status, photo, video, comments):
            return {
                'status': 201,
                'data': {
                    'id': self.details.counter - 1,
                    'message': 'Created record successfully'
                }
            }, 201
        return {
            'status': 405,
            'message': 'The URL entered is not allowed'
        }, 405

        self.details.counter += 1

    """The method gets all the records"""
    def get(self):
        get_all = self.details.get_redFlag()
        if get_all:
            return {
                'status': 200,
                'data': get_all
            }, 200
        return {
            'status': 200,
            'message': 'No record(s) found'
        }, 200


"""The class posts and gets a specific record"""


class UserReportRedFlag(Resource, RaiseRedFlagModel):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Get specific record"""
    def get(self, id):
        get_specific = self.details.find(id)
        if get_specific:
            return {
                'status': 200,
                'data': get_specific
            }, 200
        return {
            'status': 404,
            'message': 'record not found'
            }, 404

    """Deletes a specific record"""

    def delete(self, id):
        record = self.details.find(id)
        if record:
            self.details.get_redFlag().remove(record)
            return {
                    'status': 200,
                    'data': [{
                        'id': int(id),
                        'message': 'successfully deleted record'
                    }]
            }, 200

        return {
            'status': 404,
            'error': 'record not found'
        }, 404


class Patch_location(Resource, RaiseRedFlagModel):
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Edit specific record"""
    def patch(self, id):
        args = parser.parse_args()
        data = request.get_json()
        record = self.details.find(id)

        if not re.match(r"^([-+]?\d{1,2}([.]\d+)?),\s*([-+]?\d{1,3}([.]\d+)?)$\
                    ", data['location']):
            return {'message': 'Please seperate the lat and long with a comma a\
            nd should be within the range'}

        if not data['location'] or len(data['location'].split()) == 0:
            return {'message': 'Location cannot be left blank'}
        if not record:
            return {
                'status': 500,
                'message': 'location not updated'
            }, 500
        record['location'] = request.json.get('location',
                                              data['location'])
        return {
            'status': 200,
            'message': 'Succesfully updated location'
        }, 200


class Patch_comment(Resource, RaiseRedFlagModel):

    """Edit specific record"""
    def __init__(self):
        self.details = RaiseRedFlagModel()

    """Edit specific record"""
    def patch(self, id):
        args = parser.parse_args()
        data = request.get_json()
        record = self.details.find(id)

        if re.match(r"([@_!#$%^&*()<>?/\|}{~:])", data['comments']):
            return {'message': 'Invalid comments input'}

        if not data['comments'] or len(data['comments'].split()) == 0:
            return {'message': 'comments cannot be left blank'}
        if not record:
            return {
                'status': 500,
                'message': 'comments not updated'
            }, 500
        record['comments'] = request.json.get('comments',
                                              data['comments'])
        return {
            'status': 200,
            'message': 'Succesfully updated comments'
        }, 200
