""""Import statements."""
from flask_restful import fields

user_serializer = {
    'name': fields.String
}

bucketlistitem_serializer = {
    'iid': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.String
}

bucketlist_serializer = {
    'bid': fields.Integer,
    'name': fields.String,
    'items': fields.Nested(bucketlistitem_serializer),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer
}
