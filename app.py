from models.bucketlist_model import app
from resource_definitions import api, Allbucketlists, Onebucketlist, \
    Bucketlistitem, Bucketitemsactions, Login, Logout

api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(Allbucketlists, '/bucketlists/')
api.add_resource(Onebucketlist, '/bucketlists/<id>')
api.add_resource(Bucketlistitem, '/bucketlists/<id>/items/')
api.add_resource(Bucketitemsactions, '/bucketlists/<id>/items/<item_id>')

if __name__ == '__main__':
    app.run(debug=True)
