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

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class BucketList(db.Model):
    """The bucketlist model class."""
    __tablename__ = 'bucketlists'
    bid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    items = db.relationship('BucketListItem', backref='bucketlists', cascade="all", lazy="joined")
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('user.uid'))

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
