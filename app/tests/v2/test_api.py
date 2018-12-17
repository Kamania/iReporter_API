import unittest
import json
from app import create_app
from app.db_config import init_test_db, create_tables
from app.api.v2.models.record_models import RaiseRedFlagModel
from psycopg2.extras import RealDictCursor


class TestRecord(unittest.TestCase):
    def setUp(self):
            self.app = create_app()
            self.client = self.app.test_client()
            self.conn = init_test_db()
            self.incidence = {
                'type': 'redflag',
                'location': '-10.45343, 23.64543',
                'status': 'Draft',
                'comment': 'comments'
            }            

            self.app_context = self.app.app_context()
            self.app_context.push()
            
    def signup_user(self):
        self.user = {
                'firstname': 'Magda',
                'lastname': 'Muthoni',
                'othernames': 'Wangeci',
                'email': 'magda@gmail.com',
                'phoneNumber': '0723000000',
                'username': 'mutho',
                'password': '123456789'
            }
        resp = self.client.post('/api/v2/auth/signup', json=self.user,  headers={'content': 'application/json'})
        user_login = {
            'username': 'mutho',
            'password': '123456789'
        }

        return resp

        # self.token = resp.get_json()['token']
        # resp = self.client.post('/api/v2/auth/login', json=user_login,
        #                         headers={'content': 'application/json', 'authorization': 'Bearer' + self.token})       

    

    ''' Test for records '''

    def test_post_records(self):
        self.signup_user()
        resp = self.client.post('/api/v2/records',
                                data={
                                    'type': 'redflag',
                                    'location': '-10.45343, 23.64543',
                                    'status': 'Draft',
                                    'comment': 'comments'
                                })
        data = json.loads(resp.get_data(as_text=True))
        # self.assertEqual(data['message'], 'Record created successful', msg='The URL entered is not allowed')
        self.assertEqual(resp.status_code, 201)

    def test_get_all_records(self):
        self.client.post('/api/v2/records',
                         json=self.incidents.get_redFlag())
        resp = self.client.get('/api/v2/records')
        resp = self.incidents.get_redFlag()
        self.assertEqual(resp.status_code, 200)

    def test_one_get_record(self):
        resp = self.client.post('/api/v2/records',
                                json=self.records)
        resp = self.client.get('/api/v2/records/2')
        self.assertEqual(resp.status_code, 200)

    def test_patch_specific_location(self):
        resp = self.client.patch('/api/v2/records/2/location',
                                 json=self.incidence)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Succesfully updated location', msg='location not updated')
        self.assertEqual(resp.status_code, 200)

    def test_patch_specific_comment(self):
        resp = self.client.patch('/api/v2/records/2/comment',
                                 json=self.incidence)
        data = json.loads(resp.get_data(as_text=True))
        # self.assertEqual(data['message'], 'Succesfully updated comments', msg='comments not updated')
        self.assertEqual(resp.status_code, 200)

    ''' Validations tests '''
    def test_empty_comment(self):
        resp = self.client.post('/api/v2/records',
                                json={
                                    "type": "Red-Flag",
                                    "location": "22.23556, 33.4578899",
                                    "status": "Draft",
                                    "comments": " "
                                })
        data = json.loads(resp.get_data(as_text=True))
        # self.assertEqual(data['message'], 'Comments cannot be left blank')
        self.assertEqual(resp.status_code, 400)

    def test_specialChar_In_comments(self):
        resp = self.client.post('/api/v2/records',
                                json={
                                    "type": "Red-Flag",
                                    "location": "22.23556, 33.4578899",
                                    "status": "Draft",
                                    "comments": "@##$%^&&"
                                })
        data = json.loads(resp.get_data(as_text=True))
        # self.assertEqual(data['message'], 'Comment cannot contain special characters')
        self.assertEqual(resp.status_code, 400)

    def test_comma_seperation_in_location(self):
        resp = self.client.post('/api/v2/records', json={
                                                    "type": "Red-Flag",
                                                    "location": "2j2.23556, 33.45lo78899",
                                                    "status": "Draft",
                                                    "comments": "what"
                                                })
        # self.assertEqual(data['message'], 'Please ensure to seperate lat and long with a\
        #          comma, lat and long are numbers, lat and long are within\
        #          their appropriate range.')
        self.assertEqual(resp.status_code, 400)

    def test_empty_location(self):
        resp = self.client.post('/api/v2/records',
                                json={
                                    "createdOn": "12/23/17",
                                    "createdBy": "ssd",
                                    "type": "Red-Flag",
                                    "location": "    ",
                                    "status": "Draft",
                                    "photo": "image.png",
                                    "video": "wak.mp4",
                                    "comments": "what"
                                })
        data = json.loads(resp.get_data(as_text=True))
        # self.assertEqual(data['message'], 'Location cannot be left blank')

    def test_delete_specific_record(self):
        resp = self.client.post('/api/v2/records',
                                json=self.records)
        resp = self.client.delete('/api/v2/records/1', json=self.records)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'successfully deleted record')
        self.assertEqual(resp.status_code, 200)

    # ''' Tests for users'''

    # def test_user_post(self):
    #     resp = self.client.post('/api/v2/user',
    #                             json=self.u)
    #     self.assertEqual(resp.status_code, 201)

    # def test_get_all_users(self):
    #     self.client.post('/api/v2/records',
    #                      json=self.user)
    #     resp = self.client.get('/api/v2/user')
    #     self.assertEqual(resp.status_code, 200)

    # def test_get_one_user(self):
    #     resp = self.client.post('/api/v2/user',
    #                             json=self.user)
    #     resp = self.client.get('/api/v2/user/1')
    #     self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()
