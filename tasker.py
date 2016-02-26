"""Import statements."""
from models.bucketlist_model import db
from models.bucketlist_model import User, BucketList, BucketListItem

db.create_all()

adminUser = User("amos", 12345)

db.session.add(adminUser)
db.session.commit()


blist = BucketList("Life goals", 1)

db.session.add(blist)
db.session.commit()

blistitem = BucketListItem("Climb Mt. Everest", 1)

db.session.add(blistitem)
db.session.commit()
