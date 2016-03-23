""""Import statements."""
from flask_restful import fields
from collections import OrderedDict

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
