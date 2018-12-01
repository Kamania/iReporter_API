import unittest
import json
from app import create_app


def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app
        self.records = json.dumps({
            "id": 1,
            "createdOn": "12/23/2013",
            "createdBy": "Kamania",
            "type": "red-flag",
            "location": "[12.2344334, 45.323232]",            
            "status": "rejected",
            "photo": "[red.png]",
            "video": "[red.mp4]",
            "comments": "This must be sorted immediately"
        })

def test_post_all_records(self):
    resp = self.client.post('/api/v1/red_flag_records', 
                            data=self.records, 
                            # headers={"content-type": "application/json"}
                            content_type='application/json'
                            )
    result = json.loads(resp.data.decode())        
    self.assertEqual(result["message"], "Record saved successful", msg = "Record not successful saved")
    self.assertEqual(resp.status_code, 201)

def test_get_all_records(self):
        resp = self.client.get('/api/v1/red_flag_records')
        # result = json.loads(resp.data.decode())        
        # self.assertEqual(result["message"], "Successfully viewed", msg = "No records to view")
        self.assertEqual(resp.status_code, 200)