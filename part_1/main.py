import connect
from models import Authors, Quotes


def input_parser(user_input):
    command, value = user_input.strip().split(':')
    return command, value


def input_handler(command, value):
    match command:
        case 'name':
            find_author(value)
        case 'tag':
            find_tag(value)
        case 'tags':
            tags = value.strip().split(',')
            for tag in tags:
                find_tag(tag.strip())
        case _:
            print(f'Wrong command. Try again')


def find_author(author):
    author_id = Authors.objects().first()
    if author_id:
        author_id = author_id.id

    data = Quotes.objects(author=author_id)
    if data:
        for item in data:
            print(item.quote)
    else:
        print('Nothing found. Try again')


def find_tag(tag):
    tags_found = []
    data = Quotes.objects()

    if data:
        for el in data:
            for data_tag in el.tags:
                if tag == data_tag.name:
                    tags_found.append(el.quote)
        print(tags_found)
    else:
        print('Nothing found. Try again')


if __name__ == '__main__':
    while True:
        user_input = input('Input command: ')
        if user_input == 'exit':
            exit(0)
        else:
            try:
                command, value = input_parser(user_input)
                input_handler(command, value)
            except ValueError:
                print('Wrong format. Try {command}:{value}')
