"""Import statements."""
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from config.config import DevelopmentConfig

# create the flask app
app = Flask(__name__)

# configure app
app.config.from_object(DevelopmentConfig)

# create a database object instance
db = SQLAlchemy(app)


class User(db.Model):
    """The user model class."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    bucketlists = db.relationship('BucketList', backref='user',
                                  cascade="all", lazy="joined")

    def hash_password(self, password):
        return hashlib.sha224(password).hexdigest()

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def verify_password(self, password):
        hashed_password = hashlib.sha224(password).hexdigest()

        if hashed_password == self.password:
            return True

        return False

    @staticmethod
    def verify_auth_token(token):
        """Verify token and return user object."""
        s = Serializer(session['serializer_key'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class BucketList(db.Model):
    """The bucketlist model class."""

    __tablename__ = 'bucketlists'
    bid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    items = db.relationship('BucketListItem', backref='bucketlists',
                            cascade="all", lazy="joined")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __unicode__(self):
        return '<Bucketlist": {}>'.format(self.name)


class BucketListItem(db.Model):
    """The bucketlist item model class."""

    __tablename__ = 'items'
    iid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    done = db.Column(db.String(10), default='False')
    bid = db.Column(db.Integer, db.ForeignKey('bucketlists.bid'))

    def __init__(self, name, bid):
        self.name = name
        self.bid = bid

    def __repr__(self):
        return '<Bucketlist Item: {}>'.format(self.name)
