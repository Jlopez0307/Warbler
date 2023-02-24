"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] =  'postgresql://postgres:Halo03117!@localhost:5432/warbler'


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u1 = User.signup("test1", "email1@email.com", "password", None)
        u2 = User.signup("test2", "email2@email.com", "password", None)

        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_follows(self):
        """ Tests user follows"""
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertEqual(self.u2.followers[0].id, self.u1.id)
        self.assertEqual(self.u1.following[0].id, self.u2.id)

    def test_is_following(self):
        """ Tests following between two users """
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))

    def test_user_creation(self):
        test_user = User.signup("SomeUsername", "some@email.com", "password", None)
        db.session.add(test_user)
        db.session.commit()

        self.assertTrue(User.query.get(test_user.id))

    def test_failed_user_creation(self):
        test_user = User.signup(None, "some@email.com", "password", None)

        db.session.add(test_user)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_successful_auth(self):
        self.assertTrue(User.authenticate(self.u1.username, "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "notPassword"))
    
    def test_wrong_username(self):
        self.assertFalse(User.authenticate("FakeUsername", "password"))




        