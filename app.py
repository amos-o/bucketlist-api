"""Import statements."""
from models.bucketlist_model import User, BucketList, BucketListItem, app, db
from flask_restful import Resource, fields, Api, marshal_with
from flask import request, jsonify
from collections import OrderedDict

# create the api object
api = Api(app)

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
class Allbucketlists(Resource):
    @marshal_with(bucketlist_fields, envelope='bucketlists')
    def get(self):
        """Query all bucketlists."""
        bucketlists = BucketList.query.all()

        return bucketlists

    def post(self):
        """Create new bucket list."""
        json_data = request.get_json()

        name = json_data['name']
        uid = json_data['uid']

        blist = BucketList(name, uid)

        db.session.add(blist)
        db.session.commit()

        return jsonify({'message': 'Bucketlist created successfully.'})


class Onebucketlist(Resource):
    """Query one bucketlist by id."""
    @marshal_with(bucketlist_fields, envelope='bucketlists')
    def get(self, id):
        bucketlist = BucketList.query.filter_by(bid=id).first()

        return bucketlist

api.add_resource(Allbucketlists, '/bucketlists/')
api.add_resource(Onebucketlist, '/bucketlists/<id>')

if __name__ == '__main__':
    app.run(debug=True)
