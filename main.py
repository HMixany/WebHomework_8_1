import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(*args) -> list[str | None]:
    tag = args[1]
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(*args) -> list[str | None]:
    tags = args[1].split(',')
    result = []
    quotes = Quote.objects(tags__in=tags)
    result.extend([q.quote for q in quotes])
    return result


@cache
def find_by_author(*args) -> list[str | None]:
    author = args[1]
    result = []
    if author:
        authors = Author.objects(fullname__iregex=author)
        for a in authors:
            quotes = Quote.objects(author=a)
            result.extend([q.quote for q in quotes])
    else:
        raise TypeError
    return result


COMMANDS = {'name': find_by_author, 'tag': find_by_tag, 'tags': find_by_tags}


def get_handler(command):
    return COMMANDS.get(command)


def main():
    while True:
        try:
            input_user = input('Write command \t')
            if input_user.lower() == 'exit':
                print('Good bay!')
                break
            else:
                list_input = input_user.split(':')
                arguments = tuple((el.strip() for el in list_input))
                print(arguments)
                handler = get_handler(arguments[0].lower())
                print(handler(*arguments))
        except TypeError:
            print("Помилка у введенні")
        except IndexError:
            print("Помилка у введенні")


if __name__ == '__main__':
    main()

