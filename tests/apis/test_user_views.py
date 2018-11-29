from flask_testing import TestCase
from app import create_app, db
from app.models import User

class TestUserViews(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_show(self):
        self.setUp()
        first_user = User()
        first_user.username = "User1"
        first_user.apitoken = "ABCD"
        db.session.add(first_user)
        db.session.commit()
        response = self.client.get("/user/1")
        response_user = response.json
        print(response_user)
        self.assertEqual(response_user["id"], 1)
        self.assertEqual(response_user["username"], "User1")
        self.assertIsNotNone(response_user["apitoken"])
        self.tearDown()


    def test_user_create(self):
        self.setUp()
        response = self.client.post("/user", json={'username': 'User1'})
        created_user = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_user["id"], 1)
        self.assertEqual(created_user["username"], "User1")
        self.tearDown()

#    def test_tweet_update(self):
#        self.setUp()
#        first_tweet = Tweet()
#        first_tweet.text = "First tweet"
#        db.session.add(first_tweet)
#        db.session.commit()
#        response = self.client.patch("/tweets/1", json={'text': 'New text'})
#        updated_tweet = response.json
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(updated_tweet["id"], 1)
#        self.assertEqual(updated_tweet["text"], "New text")
#        self.tearDown()

    def test_user_delete(self):
        self.setUp()
        first_user = User()
        first_user.username = "User Test"
        first_user.apitoken = "XYZ"
        db.session.add(first_user)
        db.session.commit()
        self.client.delete("/user/1")
        self.assertIsNone(db.session.query(User).get(1))
        self.tearDown()

    def test_all_user_show(self):
        self.setUp()
        first_user = User()
        first_user.username = "First User"
        first_user.apitoken = "Token1"
        db.session.add(first_user)
        first_user = User()
        first_user.username = "Second User"
        first_user.apitoken = "Token2"
        db.session.add(first_user)
        db.session.commit()
        response = self.client.get("/user")
        response_user = response.json

        self.assertIsNotNone(response_user[0]["id"])
        self.assertEqual(response_user[0]["username"], "First User")
        self.assertEqual(response_user[0]["apitoken"], "Token1")
        self.assertIsNotNone(response_user[1]["id"])
        self.assertEqual(response_user[1]["username"], "Second User")
        self.assertEqual(response_user[1]["apitoken"], "Token2")
        self.tearDown()
