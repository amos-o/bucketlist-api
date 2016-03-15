"""Import statements."""
from models.bucketlist_model import User, BucketList, BucketListItem, app, db
from flask_restful import Resource, Api, marshal_with, marshal
from flask import request, jsonify, session
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask.ext.httpauth import HTTPBasicAuth
from helpers.random_string_generator import id_generator
from helpers.marshal_fields import user_fields, item_fields, bucketlist_fields

# create auth object
auth = HTTPBasicAuth()

# create the api object
api = Api(app)


# API ROUTES #
@auth.verify_password
def verify_password(token, password):
    """Take the token and verify that it is valid."""
    # authenticate by token
    token = request.headers.get('Authorization')

    if not token:
        return False

    user = User.verify_auth_token(token)

    if user:
        return True
    else:
        return False


class Login(Resource):
    def post(self):
        """Login a user and return a token."""
        # get user login data from request
        json_data = request.get_json()

        if "username" in json_data and "password" in json_data:
            # set uname and pword
            uname = json_data['username']
            pword = json_data['password']
        else:
            return {"message": "Provide both a username and a password."}, 401

        # select user from db based on username
        user = User.query.filter_by(username=uname).first()

        # check if the user's password matches the one entered
        result = user.verify_password(pword)

        # if result will be true, generate a token
        if result:
            session['user_id'] = user.id

            session['serializer_key'] = id_generator()

            s = Serializer(session['serializer_key'], expires_in=6000)
            return s.dumps({'id': user.id})

        return jsonify({"message": "Invalid login details."})


class Logout(Resource):
    @auth.login_required
    def get(self):
        # replace the serializer_key with an invalid one
        session['serializer_key'] = id_generator()
        del session['user_id']

        return jsonify({"message": "You have been logged out successfully."})


class Allbucketlists(Resource):
    @auth.login_required
    @marshal_with(bucketlist_fields, envelope='bucketlists')
    def get(self):
        """Query all bucketlists."""
        # get id of logged in user
        uid = session['user_id']

        # if limit exists, assign it to limit
        limit = request.args.get('limit')
        # if q exists, assign it to q
        q = request.args.get('q')

        if limit is not None:
            bucketlists = BucketList.query.filter_by(created_by=uid). \
                limit(limit).all()

            return bucketlists

        if q is not None:
            bucketlists = BucketList.query.filter_by(created_by=uid).all()

            # will hold all bucketlists that meet search criteria
            listOfResults = []

            for bucket in bucketlists:
                if q in bucket.name:
                    listOfResults.append(bucket)

            return listOfResults

        # if limit and search query are not specified,
        # query and return all bucketlists
        bucketlists = BucketList.query.filter_by(created_by=uid).all()

        return bucketlists

    @auth.login_required
    def post(self):
        """Create a new bucketlist."""
        # get data from json request
        json_data = request.get_json()

        # get name of bucketlist from json data
        name = json_data['name']
        # get owner id from logged in user session
        uid = session['user_id']

        # create the bucketlist using the relevant data
        blist = BucketList(name, uid)

        # commit bucketlist to db
        db.session.add(blist)
        db.session.commit()

        return jsonify({'message': 'Bucketlist created successfully.'})


class Onebucketlist(Resource):
    @auth.login_required
    def get(self, id):
        """Query one bucketlist by ID."""
        # get id of logged in user
        uid = session['user_id']

        bucketlist = BucketList.query.filter_by(created_by=uid, bid=id).first()

        if bucketlist is not None:
            return marshal(bucketlist, bucketlist_fields)

        return {"Error": "Nothing found"}, 404

    @auth.login_required
    def put(self, id):
        """Update one bucketlist using its ID."""
        # get id of logged in user
        uid = session['user_id']

        json_data = request.get_json()
        bucketlist = BucketList.query.filter_by(created_by=uid, bid=id).first()

        if bucketlist is not None:
            bucketlist.name = json_data['name']

            db.session.add(bucketlist)
            db.session.commit()

            return marshal(bucketlist, bucketlist_fields)

        return {"Error": "Bucketlist not found"}, 404

    @auth.login_required
    def delete(self, id):
        """Delete a bucketlist using its ID."""
        # get id of logged in user
        uid = session['user_id']

        bucketlist = BucketList.query.filter_by(created_by=uid, bid=id).first()

        if bucketlist is not None:
            db.session.delete(bucketlist)
            db.session.commit()

            return jsonify({'message': 'Bucketlist ' + id +
                            ' deleted successfully.'})

        return {"Error": "Bucketlist not found"}, 404


class Bucketlistitem(Resource):
    """
    Handle creation of new bucketlist items.

    Resource url:
        '/bucketlists/<id>/items/'
    Endpoint:
        'items'

    Requests Allowed:
        POST
    """

    @auth.login_required
    def post(self, id):
        """Create a new bucketlist item."""
        # get id of logged in user
        uid = session['user_id']

        # get the data for new item from request
        json_data = request.get_json()

        # item data
        itemname = json_data['name']

        # confirm user actually owns the bucketlist to be modified
        bucketlist = BucketList.query.filter_by(created_by=uid, bid=id).first()

        if bucketlist is not None:
            # create the new bucketlist item
            newitem = BucketListItem(itemname, id)
        else:
            return {"message": "You do not own a"
                    " " + "bucketlist with id " + str(id)}, 401

        # save the item in the database
        db.session.add(newitem)
        db.session.commit()

        # get the updated bucketlist and return it
        updatedBucketList = \
            BucketList.query.filter_by(created_by=uid, bid=id).first()

        return marshal(updatedBucketList, bucketlist_fields)


class Bucketitemsactions(Resource):
    """Put and Delete methods for bucketlist items."""

    @auth.login_required
    # @marshal_with(item_fields, envelope='item')
    def put(self, id, item_id):
        """Update a bucketlist item."""
        # get id of logged in user
        uid = session['user_id']

        # select the item from database for modification
        bucketlist = BucketList.query.filter_by(created_by=uid, bid=id).first()

        # if logged in user owns the bucketlist
        if bucketlist:
            item = BucketListItem.query.filter_by(bid=id, iid=item_id).first()

            # get update data from request
            json_data = request.get_json()

            # update item
            if item is not None:
                item.name = json_data['name']

                db.session.add(item)
                db.session.commit()

                return marshal(item, item_fields)

        return {"Error": "Bucketlist item not found"}, 404

    @auth.login_required
    def delete(self, id, item_id):
        """Delete a bucketlist item using its ID."""
        # get id of logged in user
        uid = session['user_id']

        # select the item from database for modification
        bucketlist = BucketList.query.filter_by(created_by=uid, bid=id).first()

        if bucketlist:
            item = BucketListItem.query.filter_by(bid=id, iid=item_id).first()

            if item:
                db.session.delete(item)
                db.session.commit()

                return jsonify({'message': 'Item ' + item_id +
                                ' from bucketlist ' + id +
                                ' deleted successfully.'})
            else:
                return {"Error": "Bucketlist has"
                        " " + "no item with id " + str(item_id)}, 404

        return {"Error": "Bucketlist not found"}, 404

# ADD RESOURCES TO API OBJECT
api.add_resource(Allbucketlists, '/bucketlists/', endpoint='bucketlists')
api.add_resource(Onebucketlist, '/bucketlists/<id>', endpoint='bucketlist')
api.add_resource(Bucketlistitem, '/bucketlists/<id>/items/', endpoint='items')
api.add_resource(Bucketitemsactions, '/bucketlists/<id>/items/<item_id>',
                 endpoint='item')
api.add_resource(Login, '/auth/login', endpoint='login')
api.add_resource(Logout, '/auth/logout', endpoint='logout')
