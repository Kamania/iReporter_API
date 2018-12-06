import unittest
import json
from app import create_app


class TestRecord(unittest.TestCase):
    def setUp(self):
            self.app = create_app()
            self.client = self.app.test_client()
            self.app_context = self.app
            self.records = json.dumps({
                "id": 1,
                "createdOn": "12/23/17",
                "createdBy": "ssd",
                "type": "Red-Flag",
                "location": "22.23556 33.4578899",
                "status": "Draft",
                "photo": "image.png",
                "video": "wak.mp4",
                "comments": "what"
            })

    def test_post_all_records(self):
        resp = self.client.post('/api/v1/records',
                                data=self.records,
                                content_type='application/json'
                                )
        self.assertEqual(resp.status_code, 201)

    def test_get_all_records(self):
        self.client.post('/api/v1/records',
                         data=self.records,
                         content_type='application/json'
                         )
        resp = self.client.get('/api/v1/records')
        self.assertEqual(resp.status_code, 200)

    def test_one_get_record(self):
        resp = self.client.get('/api/v1/records/1')
        self.assertEqual(resp.status_code, 200)

    def test_patch_specific_location(self):
        resp = self.client.patch('/api/v1/records/1/location')
        self.assertEqual(resp.status_code, 200)

    def test_patch_specific_comment(self):
        resp = self.client.patch('/api/v1/records/1/comment')
        self.assertEqual(resp.status_code, 200)


class TestDeleteRecord(unittest.TestCase):
    def setUp(self):
            self.app = create_app()
            self.client = self.app.test_client()
            self.app_context = self.app
            self.records = json.dumps({
                "id": 1,
                "createdOn": "12/23/17",
                "createdBy": "ssd",
                "type": "Red-Flag",
                "location": "22.23556 33.4578899",
                "status": "Draft",
                "photo": "image.png",
                "video": "wak.mp4",
                "comments": "what"
            })

    def test_delete_specific_record(self):
        resp = self.client.delete('/api/v1/records/1')
        self.assertEqual(resp.status_code, 200)
