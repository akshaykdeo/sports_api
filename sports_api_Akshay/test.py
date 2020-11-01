# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 21:47:45 2020

@author: Akshay
"""
import unittest
from sports_api import app
import json

class FlaskTest(unittest.TestCase):
    
    #####Methods for Use Case 1 :Retrieve match by id:
    #Check response codes for use cases
    def test_codes_1(self):
        tester = app.test_client(self)
        resp = tester.get("/match/8661032861909884224")
        statuscode = resp.status_code
        self.assertEqual(statuscode,200)   
        
    #Check for Data returned
    def test_content_1(self):
        tester = app.test_client(self)
        resp = tester.get("/match/8661032861909884224")
        self.assertEqual(resp.content_type, "application/json")
    
    #Check for Data returned
    def test_data1(self):
        tester = app.test_client(self)
        resp = tester.get("/match/8661032861909884224")
        self.assertTrue(b'id' in resp.data)
    
    
    
    #####Methods for Use Case 2 :Retrieve football matches ordered by start_time:
    #Check response codes for use cases
    def test_codes_2(self):
        tester = app.test_client(self)
        resp = tester.get("/match/?sport=football&ordering=startTime")
        statuscode = resp.status_code
        self.assertEqual(statuscode,200)   
        
    #Check for Data returned
    def test_content_2(self):
        tester = app.test_client(self)
        resp = tester.get("/match/?sport=football&ordering=startTime")
        self.assertEqual(resp.content_type, "application/json")
    
    #Check for Data returned
    def test_data2(self):
        tester = app.test_client(self)
        resp = tester.get("/match/?sport=football&ordering=startTime")
        self.assertTrue(b'id' in resp.data)
        
        
        
    #####Methods for Use Case 3 :Retrieve matches filtered by name:
    #Check response codes for use cases
    def test_codes_3(self):
        tester = app.test_client(self)
        resp = tester.get("/match/?name=Real%20Madrid%20vs%20Barcelona")
        statuscode = resp.status_code
        self.assertEqual(statuscode,200)   
        
    #Check for Data returned
    def test_content_3(self):
        tester = app.test_client(self)
        resp = tester.get("/match/?name=Real%20Madrid%20vs%20Barcelona")
        self.assertEqual(resp.content_type, "application/json")
    
    #Check for Data returned
    def test_data3(self):
        tester = app.test_client(self)
        resp = tester.get("/match/?name=Real%20Madrid%20vs%20Barcelona")
        self.assertTrue(b'id' in resp.data)
        
      
        
    ######Check response code for post method 
    def test_post_resp(self):
        tester = app.test_client(self)
        mock_request_data = {
                 "id": 8661032861909884224,
                 "message_type": "NewEvent",
                 "event": {
                         "id": 994839351740,
                         "name": "Real Madrid vs Barcelona",
                         "startTime": "2018-06-20 10:30:00",
                         "sport": {
                                 "id": 221,
                                 "name": "Football"
                                 },
                                 "markets": [
                                         {
                                                 "id": 385086549360973392,
                                                 "name": "Winner",
                                                 "selections": [
                                                         {
                                                                 "id": 8243901714083343527,
                                                                 "name": "Real Madrid",
                                                                 "odds": 1.01
                                                                 },
                                                                 {
                                                                         "id": 5737666888266680774,
                                                                         "name": "Barcelona",
                                                                         "odds": 1.01
                                                                         }
                                                                 ]
                                                 }
                                                 ]
                                                 }
                                    }      

    
        response = tester.post("/add", data=json.dumps(mock_request_data))
        assert response.status_code == 200
    
if __name__ == '__main__':
    unittest.main()
        