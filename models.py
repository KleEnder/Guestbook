from google.appengine.ext import ndb

class Guestbook(ndb.Model):
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.TextProperty()
    date = ndb.DateTimeProperty()
    deleted = ndb.BooleanProperty(default=False)

