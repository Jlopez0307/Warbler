
import os
from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] =  'postgresql://postgres:Halo03117!@localhost:5432/warbler'



from app import app


db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            html = "@testuser"
        
            self.assertIn(html, resp.data)

    def test_show_user_details(self):
        with self.client as c:
            resp = c.get(f'/users/{self.testuser.id}')
            html = "@testuser"

            self.assertIn(html, resp.data)

    


    