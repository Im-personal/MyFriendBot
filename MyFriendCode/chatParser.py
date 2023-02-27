from bs4 import BeautifulSoup


class Message:
    def __init__(self, text, user, date):
        self.text = text
        self.user = user
        self.date = date


class User:
    def __init__(self, name):
        self.name = name


class Chat:
    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)


def html_chat_parser(path):
    chat = open(path, 'r',encoding='utf-8')
    data = chat.read()
    soup = BeautifulSoup(data, 'html.parser')
    messages = soup.find_all(class_='clearfix')

    res = Chat()

    for msg in messages:
        print(msg)
        body = msg.find('body')
        user = User(body.find('from_name').text)
        text = body.find('text').text
        date = body.find('date')['title']
        n_mes = Message(text, user, date)
        res.append(n_mes)

    chat.close()
    return res
