import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows,Likes

os.environ['DATABASE_URL'] =  'postgresql://postgres:Halo03117!@localhost:5432/warbler'

from app import app

db.create_all()


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u1 = User.signup("test1", "email1@email.com", "password", None)
        db.session.add(u1)
        db.session.commit()

        self.u1 = u1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):
        message = Message(
            text = "A random warble",
            user_id = self.u1.id
        )

        db.session.add(message)
        db.session.commit()

        self.assertTrue(Message.query.get(message.id))

    def test_message_likes(self):
        message = Message(
            text = "A random warble",
            user_id = self.u1.id
        )

        db.session.add(message)
        db.session.commit()

        self.u1.likes.append(message)
        
        like = Likes.query.filter(Likes.user_id == self.u1.id).all()

        self.assertEqual(len(like), 1)
