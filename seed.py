import json
from mongoengine.errors import NotUniqueError
from models import Author, Quote


def insert_authors():
    with open('authors.json', encoding='utf-8') as fh:
        data = json.load(fh)
        for el in data:
            try:
                author = Author(
                    fullname=el.get('fullname'),
                    born_date=el.get('born_date'),
                    born_location=el.get('born_location'),
                    description=el.get('description'),
                )
                author.save()
            except NotUniqueError:
                print(f"Автор {el.get('fullname')} вже існує")


def insert_quotes():
    with open('quotes.json', encoding='utf-8') as fh:
        data = json.load(fh)
        for el in data:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(
                author=author,
                tags=el.get('tags'),
                quote=el.get('quote'),
            )
            quote.save()


if __name__ == '__main__':
    insert_authors()
    insert_quotes()
