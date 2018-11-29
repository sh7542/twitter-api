from flask_restplus import Namespace, Resource, fields
from flask import abort
from app import db
from app.models import User
from secrets import token_urlsafe

api = Namespace('user')

json_user = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'apitoken': fields.String
})

json_new_user = api.model('New User', {
    'username': fields.String(required=True)
})

@api.route('/<int:id>')
@api.response(404, 'User not found')
@api.param('id', 'The user unique identifier')
class UserResource(Resource):
    @api.marshal_with(json_user)
    def get(self, id):
        user = db.session.query(User).get(id)
        db.session.commit()
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            return user

#    @api.marshal_with(json_tweet, code=200)
#    @api.expect(json_new_tweet, validate=True)
#    def patch(self, id):
#        tweet = db.session.query(Tweet).get(id)
#        db.session.commit()
#        if tweet is None:
#            api.abort(404, "Tweet {} doesn't exist".format(id))
#        else:
#            tweet.text = api.payload["text"]
#            return tweet
#
    def delete(self, id):
        user = db.session.query(User).get(id)
        db.session.commit()
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            db.session.delete(user)
            db.session.commit()
            return None

@api.route('')
@api.response(422, 'Invalid user')
class UserResource(Resource):
    @api.marshal_with(json_user, code=201)
    @api.expect(json_new_user, validate=True)
    def post(self):
        text = api.payload["username"]
        if len(text) > 0:
            user = User()
            user.username = text
            user.apitoken = token_urlsafe(20)
            db.session.add(user)
            db.session.commit()
            return user, 201
        else:
            return abort(422, "User username can't be empty")

    @api.marshal_with(json_user, code=200)
    def get(self):
        users = db.session.query(User).all()
        db.session.commit()
        return users

