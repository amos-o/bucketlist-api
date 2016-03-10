"""Import statements."""
from models.bucketlist_model import db
from models.bucketlist_model import User, BucketList, BucketListItem

db.create_all()

# create test users
adminUser = User("amos", "12345")

db.session.add(adminUser)
db.session.commit()

user2 = User("omondi", "12345")

db.session.add(user2)
db.session.commit()

# give test users bucketlists
# for adminUser
blist = BucketList("Life goals", 1)

db.session.add(blist)
db.session.commit()

blistitem = BucketListItem("Climb Mt. Everest", 1)

db.session.add(blistitem)
db.session.commit()

# for user2
blist2 = BucketList("Movies to watch", 2)

db.session.add(blist2)
db.session.commit()

blistitem2 = BucketListItem("The pursuit of happyness", 2)

db.session.add(blistitem2)
db.session.commit()
