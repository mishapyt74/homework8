from mongoengine import connect, Document, StringField, ReferenceField, ListField

connect('your_db_name', host='your_connection_string')

class Author(Document):
    name = StringField(required=True)
    birth_date = StringField()
    birth_place = StringField()
    bio = StringField()

class Quote(Document):
    text = StringField(required=True)
    tags = ListField(StringField())
    author = ReferenceField(Author)

def load_data_to_db():
    with open('authors.json', 'r', encoding='utf-8') as authors_file:
        authors_data = json.load(authors_file)
        for author_info in authors_data:
            author = Author(**author_info)
            author.save()

    with open('quotes.json', 'r', encoding='utf-8') as quotes_file:
        quotes_data = json.load(quotes_file)
        for quote_info in quotes_data:
            author_name = quote_info.pop('author')
            author = Author.objects.get(name=author_name)
            quote_info['author'] = author
            quote = Quote(**quote_info)
            quote.save()

def search_quotes(query):
    if query.startswith('name:'):
        author_name = query.split(':')[-1].strip()
        author = Author.objects.get(name=author_name)
        quotes = Quote.objects.filter(author=author)
        return quotes
    elif query.startswith('tag:'):
        tag = query.split(':')[-1].strip()
        quotes = Quote.objects.filter(tags=tag)
        return quotes
    elif query.startswith('tags:'):
        tags = query.split(':')[-1].strip().split(',')
        quotes = Quote.objects.filter(tags__in=tags)
        return quotes
    else:
        return []

while True:
    user_input = input("Введіть команду: ")
    if user_input == 'exit':
        break
    quotes = search_quotes(user_input)
    for quote in quotes:
        print(quote.text)
