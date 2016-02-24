"""Import statements."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create the flask app
app = Flask(__name__)

# configure app database uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bucketlist.db'

# create a database object instance
db = SQLAlchemy(app)


class User(db.Model):
    """The user model class."""

    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class BucketList(db.Model):
    """The bucketlist model class."""

    bid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateIime, default=datetime.utcnow,
                              onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.uid'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Bucketlist: {}'.format(self.name)


class BucketListItem(db.Model):
    """The bucketlist tiem model class."""

    iid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateIime, default=datetime.utcnow,
                              onupdate=datetime.utcnow)
    done = db.Column(db.String(10), default='False')
    bid = db.Column(db.Integer, db.ForeignKey('bucketlist.uid'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Bucketlist Item: {}'.format(self.name)
