import gridfs
import json
#from constants import *

from bson.objectid import ObjectId

from mongoengine import *

import datetime


class Post(Document):
    NetworkId = ObjectIdField()
    FriendId = ObjectIdField()
    UserId = ObjectIdField()
    ParentId = ObjectIdField()
    Hotness = FloatField()
    Message = StringField()
    Time = DateTimeField(default=datetime.datetime.now)
    Upvotes = IntField()
    Downvotes = IntField()
    Reply = ListField(EmbeddedDocumentField('Reply'))
