"""Import statements."""
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
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
    """
    The user model class.

    Attributes:
        id: The user id.
        username: The user's username.
        bucketlists: Relationship field between the user and his bucketlists.

    Methods:
        hash_password: Hashes a new user's password.
        __init__: Initializes a new user.
        __repr__: Representation of a user.
        verify_password: Verify a user password.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    bucketlists = db.relationship('BucketList', backref='user',
                                  cascade="all", lazy="joined")

    def hash_password(self, password):
        """
        Hash a new user's password.

        Args:
            self
            password: The password to be hashed.

        Returns:
            The hashed password.
        """
        return hashlib.sha224(password).hexdigest()

    def __init__(self, username, password):
        """
        Initialize a user.

        Args:
            self
            username: Username of the new user.
            password: Password of the user.
        """
        self.username = username
        self.password = self.hash_password(password)

    def __repr__(self):
        """
        Create a string representation of a user.

        Args:
            self

        Returns:
            A string containing the user's username.
        """
        return '<User: {}>'.format(self.username)

    def verify_password(self, password):
        """
        Check that password supplied when logging in is valid.

        Args:
            self
            password: Password input by user who is logging in.

        Returns:
            True if password hashes matches
            False if password hashes do not match.
        """
        hashed_password = hashlib.sha224(password).hexdigest()

        if hashed_password == self.password:
            return True

        return False

    @staticmethod
    def verify_auth_token(token):
        """
        Verify token and return user object.

        Args:
            token: The token to be verified.

        Returns:
            A user object if token is valid.
            None if error occurs.
        """
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
    """
    The bucketlist model class.

    Attributes:
        bid: The id of the bucketlist.
        name: The name of the bucketlist.
        items: Relationship field between the bucketlist and its items.
        date_created: Date bucketlist was created.
        date_modified: Date bucketlist was modified.
        created_by: ID of user who created the bucketlist.

    Methods:
        __init__: Initializes a new bucketlist.
        __unicode__: Representation of a bucketlist.
    """

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
        """
        Initialize a bucketlist.

        Args:
            self
            name: Name of the item.
            created_by: ID of creator.
        """
        self.name = name
        self.created_by = created_by

    def __unicode__(self):
        """
        Create a string representation of a bucketlist.

        Args:
            self

        Returns:
            A string containing the bucketlist name.
        """
        return '<Bucketlist": {}>'.format(self.name)


class BucketListItem(db.Model):
    """
    The bucketlist item model class.

    Attributes:
        iid: The id of the bucketlist item.
        name: The name of the bucketlist item.
        date_created: Date bucketlist item was created.
        date_modified: Date bucketlist item was modified.
        bid: ID of bucketlist which owns the item.

    Methods:
        __init__: Initializes a new bucketlist.
        __repr__: Representation of a bucketlist.
    """

    __tablename__ = 'items'
    iid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    done = db.Column(db.String(10), default='False')
    bid = db.Column(db.Integer, db.ForeignKey('bucketlists.bid'))

    def __init__(self, name, bid):
        """
        Initialize a bucketlist item.

        Args:
            self
            name: Name of the item.
            bid: ID of parent bucketlist.
        """
        self.name = name
        self.bid = bid

    def __repr__(self):
        """
        Create a string representation of a bucketlist item.

        Args:
            self

        Returns:
            A string containing the bucketlist item name.
        """
        return '<Bucketlist Item: {}>'.format(self.name)
