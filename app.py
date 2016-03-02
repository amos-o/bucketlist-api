"""Import statements."""
from models.bucketlist_model import User, BucketList, BucketListItem, app, db
from flask_restful import Resource, fields, Api, marshal_with

# create the api object
api = Api(app)

# marshal fields
user_fields = {
    'name': fields.String,
}

item_fields = {
    'iid': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.String
}

bucketlist_fields = {
    'bid': fields.Integer,
    'name': fields.String,
    'items': fields.Nested(item_fields),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer
}

# API ROUTES #
class Allbucketlists(Resource):
    @marshal_with(bucketlist_fields, envelope='bucketlists')
    def get(self):
        bucketlists = BucketList.query.all()

        return bucketlists

api.add_resource(Allbucketlists, '/bucketlists/')

if __name__ == '__main__':
    app.run(debug=True)
