from mongoengine import connect, Document, StringField, IntField, ListField, DoesNotExist, ReferenceField, CASCADE

username = "userweb17"
password = 321456
db = "WHW_8"
host = f"mongodb+srv://{username}:{password}@cluster0.r7yz0bl.mongodb.net/?retryWrites=true&w=majority"
connect(db=db, host=host)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=20))
    quote = StringField()
    meta = {"collection": "quotes"}
