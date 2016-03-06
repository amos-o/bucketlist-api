"""Import statements."""
from models.bucketlist_model import User, BucketList, BucketListItem, app, db
from flask_restful import Resource, fields, Api, marshal_with
from flask import request, jsonify, session
from collections import OrderedDict
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask.ext.httpauth import HTTPBasicAuth
from random_string_generator import id_generator

# create auth object
auth = HTTPBasicAuth()

# create the api object
api = Api(app)

# secret key to encrypt session variables
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

# marshal fields
user_fields = OrderedDict()
user_fields['name'] = fields.String

item_fields = OrderedDict()
item_fields['iid'] = fields.Integer
item_fields['name'] = fields.String
item_fields['date_created'] = fields.DateTime
item_fields['date_modified'] = fields.DateTime
item_fields['done'] = fields.String

bucketlist_fields = OrderedDict()
bucketlist_fields['bid'] = fields.Integer
bucketlist_fields['name'] = fields.String
bucketlist_fields['items'] = fields.Nested(item_fields)
bucketlist_fields['date_created'] = fields.DateTime
bucketlist_fields['date_modified'] = fields.DateTime
bucketlist_fields['created_by'] = fields.Integer


# API ROUTES #
@auth.verify_password
def verify_password(token, password):
    """Takes the token and verifies that it is valid."""
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

        # set uname and pword
        uname = json_data['username']
        pword = json_data['password']

        # select user from db based on username
        user = User.query.filter_by(username=uname).first()

        # check if the user's password matches the one entered
        result = user.verify_password(pword)

        # if result will be true, generate a token
        if result:
            session['serializer_key'] = id_generator()

            s = Serializer(session['serializer_key'], expires_in=6000)
            return s.dumps({'id': user.id})

        return jsonify({"message": "Invalid login details."})


class Logout(Resource):
    @auth.login_required
    def get(self):
        # replace the serializer_key with an invalid one
        session['serializer_key'] = id_generator()

        return jsonify({"message": "You have been logged out successfully."})


class Allbucketlists(Resource):
    @auth.login_required
    @marshal_with(bucketlist_fields, envelope='bucketlists')
    def get(self):
        """Query all bucketlists."""
        bucketlists = BucketList.query.all()

        return bucketlists

    @auth.login_required
    def post(self):
        """Create a new bucketlist."""
        json_data = request.get_json()

        name = json_data['name']
        uid = json_data['uid']

        blist = BucketList(name, uid)

        db.session.add(blist)
        db.session.commit()

        return jsonify({'message': 'Bucketlist created successfully.'})


class Onebucketlist(Resource):
    @auth.login_required
    @marshal_with(bucketlist_fields, envelope='bucketlists')
    def get(self, id):
        """Query one bucketlist by ID."""
        bucketlist = BucketList.query.filter_by(bid=id).first()

        return bucketlist

    @auth.login_required
    @marshal_with(bucketlist_fields, envelope='bucketlists')
    def put(self, id):
        """Update one bucketlist using its ID."""
        json_data = request.get_json()
        bucketlist = BucketList.query.filter_by(bid=id).first()

        if bucketlist is not None:
            bucketlist.name = json_data['name']

            db.session.add(bucketlist)
            db.session.commit()

            return bucketlist

        return {"Error": "Bucketlist not found"}, 404

    @auth.login_required
    def delete(self, id):
        """Delete a bucketlist using its ID."""
        bucketlist = BucketList.query.get(id)

        db.session.delete(bucketlist)
        db.session.commit()

        return jsonify({'message': 'Bucketlist ' + id +
                        ' deleted successfully.'})


class Bucketlistitem(Resource):
    @auth.login_required
    @marshal_with(bucketlist_fields, envelope='bucketlists')
    def post(self, id):
        """Create a new bucketlist item."""
        # get the data for new item from request
        json_data = request.get_json()

        # item data
        itemname = json_data['name']

        # create the new bucketlist item
        newitem = BucketListItem(itemname, id)

        # save the item in the database
        db.session.add(newitem)
        db.session.commit()

        # get the updated bucketlist and return it
        updatedBucketList = BucketList.query.filter_by(bid=id).first()

        return updatedBucketList


class Bucketitemsactions(Resource):
    """Put and Delete methods for bucketlist items."""

    @auth.login_required
    @marshal_with(item_fields, envelope='item')
    def put(self, id, item_id):
        """Update a bucketlist item."""
        # select the item from database for modification
        item = BucketListItem.query.filter_by(bid=id, iid=item_id).first()

        # get update data from request
        json_data = request.get_json()

        # update item
        if item is not None:
            item.name = json_data['name']

            db.session.add(item)
            db.session.commit()

            return item

        return {"Error": "Bucketlist item not found"}, 404

    @auth.login_required
    def delete(self, id, item_id):
        """Delete a bucketlist item using its ID."""
        item = BucketListItem.query.filter_by(bid=id, iid=item_id).first()

        db.session.delete(item)
        db.session.commit()

        return jsonify({'message': 'Item ' + item_id +
                        ' from bucketlist ' + id +
                        ' deleted successfully.'})

api.add_resource(Allbucketlists, '/bucketlists/')
api.add_resource(Onebucketlist, '/bucketlists/<id>')
api.add_resource(Bucketlistitem, '/bucketlists/<id>/items/')
api.add_resource(Bucketitemsactions, '/bucketlists/<id>/items/<item_id>')
api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')

if __name__ == '__main__':
    app.run(debug=True)
