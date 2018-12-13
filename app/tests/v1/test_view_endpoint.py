import unittest
import json
from app import create_app


class TestRecord(unittest.TestCase):
    def setUp(self):
            self.app = create_app()
            self.client = self.app.test_client()
            self.app_context = self.app.app_context()
            self.app_context.push()

            ''' Record data to be usd while testing '''

            self.records = {
                "id": 1,
                "createdOn": "12/23/17",
                "createdBy": "ssd",
                "type": "Red-Flag",
                "location": "22.23556, 33.4578899",
                "status": "Draft",
                "photo": "image.png",
                "video": "wak.mp4",
                "comments": "what"
            }

            ''' User data to be used while testing '''

            self.user = {
                'id': 1,
                'firstname': 'Joseph',
                'lastname': 'Chiira',
                'othernames': 'Kamania',
                'email': 'kamania@gmail.com',
                'phoneNumber': '702643312',
                'username': 'kamania',
                'registeredOn': '12/06/18',
                'isAdmin': 'False',
                'password': '123456789',
                'password_confirmation': '123456789'
            }

    ''' Test for records '''

    def test_post_records(self):
        resp = self.client.post('/api/v1/records',
                                json=self.records)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Record created successful', msg='The URL entered is not allowed')
        self.assertEqual(resp.status_code, 201)

    def test_get_all_records(self):
        self.client.post('/api/v1/records',
                         json=self.records)
        resp = self.client.get('/api/v1/records')
        self.assertEqual(resp.status_code, 200)

    def test_one_get_record(self):
        resp = self.client.post('/api/v1/records',
                                json=self.records)
        resp = self.client.get('/api/v1/records/2')
        self.assertEqual(resp.status_code, 200)

    def test_patch_specific_location(self):
        resp = self.client.patch('/api/v1/records/2/location',
                                 json=self.records)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Succesfully updated location', msg='location not updated')
        self.assertEqual(resp.status_code, 200)

    def test_patch_specific_comment(self):
        resp = self.client.patch('/api/v1/records/2/comment',
                                 json=self.records)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Succesfully updated comments', msg='comments not updated')
        self.assertEqual(resp.status_code, 200)

    ''' Validations tests '''
    def test_empty_comment(self):
        resp = self.client.post('/api/v1/records',
                                json={
                                    "createdOn": "12/23/17",
                                    "createdBy": "ssd",
                                    "type": "Red-Flag",
                                    "location": "22.23556, 33.4578899",
                                    "status": "Draft",
                                    "photo": "image.png",
                                    "video": "wak.mp4",
                                    "comments": " "
                                })
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Comments cannot be left blank')
        self.assertEqual(resp.status_code, 400)

    def test_specialChar_In_comments(self):
        resp = self.client.post('/api/v1/records',
                                json={
                                    "createdOn": "12/23/17",
                                    "createdBy": "ssd",
                                    "type": "Red-Flag",
                                    "location": "22.23556, 33.4578899",
                                    "status": "Draft",
                                    "photo": "image.png",
                                    "video": "wak.mp4",
                                    "comments": "@#$%^&*"
                                })
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Comment cannot contain special characters')
        self.assertEqual(resp.status_code, 400)

    def test_comma_seperation_in_location(self):
        resp = self.client.post('/api/v1/records',
                                json={
                                    "createdOn": "12/23/17",
                                    "createdBy": "ssd",
                                    "type": "Red-Flag",
                                    "location": "2w2.23556, 33e.4578899",
                                    "status": "Draft",
                                    "photo": "image.png",
                                    "video": "wak.mp4",
                                    "comments": "what"
                                })
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Please ensure to seperate lat and long with a\
                 comma, lat and long are numbers, lat and long are within\
                 their appropriate range.')
        self.assertEqual(resp.status_code, 400)

    def test_empty_location(self):
        resp = self.client.post('/api/v1/records',
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
        self.assertEqual(data['message'], 'Location cannot be left blank')

    def test_empty_createBy(self):
        resp = self.client.post('/api/v1/records',
                                json={
                                    "createdOn": "12/23/17",
                                    "createdBy": " ",
                                    "type": "Red-Flag",
                                    "location": "22.23556, 33.4578899",
                                    "status": "Draft",
                                    "photo": "image.png",
                                    "video": "wak.mp4",
                                    "comments": "what"
                                })
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'CreatedBy cannot be left blank')

    def test_specialChar_In_createdBy(self):
        resp = self.client.post('/api/v1/records',
                                json={
                                    "createdOn": "12/23/17",
                                    "createdBy": "@#$%^&*",
                                    "type": "Red-Flag",
                                    "location": "22.23556, 33.4578899",
                                    "status": "Draft",
                                    "photo": "image.png",
                                    "video": "wak.mp4",
                                    "comments": "what"
                                })
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Name cannot contain special characters')
        self.assertEqual(resp.status_code, 400)

    def test_empty_createOn(self):
        resp = self.client.post('/api/v1/records',
                                json={
                                    "createdOn": " ",
                                    "createdBy": "mwas",
                                    "type": "Red-Flag",
                                    "location": "22.23556, 33.4578899",
                                    "status": "Draft",
                                    "photo": "image.png",
                                    "video": "wak.mp4",
                                    "comments": "what"
                                })
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'Date cannot be left blank')

    def test_specialChar_In_createOn(self):
        resp = self.client.post('/api/v1/records',
                                json={
                                    "createdOn": ")(*&^%$#",
                                    "createdBy": "mwas",
                                    "type": "Red-Flag",
                                    "location": "22.23556, 33.4578899",
                                    "status": "Draft",
                                    "photo": "image.png",
                                    "video": "wak.mp4",
                                    "comments": "what"
                                })

    def test_delete_specific_record(self):
        resp = self.client.post('/api/v1/records',
                                json=self.records)
        resp = self.client.delete('/api/v1/records/1', json=self.records)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data['message'], 'successfully deleted record')
        self.assertEqual(resp.status_code, 200)

    # ''' Tests for users'''

    # def test_user_post(self):
    #     resp = self.client.post('/api/v1/user',
    #                             json=self.user)
    #     self.assertEqual(resp.status_code, 201)

    # def test_get_all_users(self):
    #     self.client.post('/api/v1/records',
    #                      json=self.user)
    #     resp = self.client.get('/api/v1/user')
    #     self.assertEqual(resp.status_code, 200)

    # def test_get_one_user(self):
    #     resp = self.client.post('/api/v1/user',
    #                             json=self.user)
    #     resp = self.client.get('/api/v1/user/1')
    #     self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()
