from datetime import datetime, timezone
from mongoengine import Document, StringField, URLField, ObjectIdField, DateTimeField, EmailField



class Creators(Document):
    _id = ObjectIdField()
    ip = StringField()
    user_agent = StringField()
    time = StringField()
    original_url = URLField()
    short_url = StringField()
    tracking_url = StringField()
    
class Visitors(Document):
    _id = ObjectIdField()
    time = StringField()
    ip = StringField()
    user_agent = StringField()
    browser = StringField()
    os = StringField()
    device = StringField()
    country = StringField()
    state = StringField()
    city = StringField()
    isp = StringField()
    timezone = StringField()
    tracking_url = StringField()
    
class Contact(Document):
    _id = ObjectIdField()
    name = StringField(max_length=30)
    email = EmailField()
    message = StringField()
    time = StringField()
    

    

    