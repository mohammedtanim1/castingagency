import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Users


class castingagencytest(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path ="postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def viewusersvalidURL(self):
        res = self.client().get("/viewusers")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "Resources found")

    def viewusersinvalidURL(self):
        res = self.client().get("/viewusers12")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "pagenotfound")




    def createvalidparameters(self):
        headers = {'Authorization': 'Bearer ' + self.valid_token}
        res = self.client().post("/createuser/Tanim/Tanom1@example.com/male",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "Resources found")

    def createinvalidparameters(self):
        headers = {'Authorization': 'Bearer ' + self.valid_token}
        res = self.client().post("/createuser/Tanim1",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "pagenotfound")




    def deleteexisitingid(self):
        headers = {'Authorization': 'Bearer ' + self.valid_token}
        res = self.client().delete("/deleteuser/1",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "delete success")

    def deletenonexisitingid(self):
        headers = {'Authorization': 'Bearer ' + self.valid_token}
        res = self.client().delete("/deleteuser/tanim",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "pagenotfound")





    def patchexisitingid(self):
        headers = {'Authorization': 'Bearer ' + self.valid_token}
        res = self.client().patch("updateuser/1/Tanim",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "patch success")

    def patchnonexisitingid(self):
        headers = {'Authorization': 'Bearer ' + self.valid_token}
        res = self.client().patch("/updateuser/rat",headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "pagenotfound")


    def unauthorized_post(self):
        headers = {'Authorization': 'Bearer ' + self.invalid_token}
        res = self.client().post("/createuser/Tanim/Tanom1@example.com/male", headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()