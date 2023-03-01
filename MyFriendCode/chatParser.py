import json
import os
from datetime import datetime
import re

from bs4 import BeautifulSoup


class Message:
    def __init__(self, text, user, date):
        self.text = text  # .replace('<br/>','\n')
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

    def merge(self, chat):
        self.messages += chat.messages

    def get_chat_array(self):
        res = []
        last_name = self.messages[0].user.name

        txt = ""

        for msg in self.messages:
            if(last_name==msg.user.name):
                txt+=f"{(msg.date.strftime('%H:%M:%S'))}: {msg.text}\n"
            else:
                res.append(txt)
                txt="";
                last_name=msg.user.name
                txt += f"{(msg.date.strftime('%H:%M:%S'))}: {msg.text}\n"
        return res


def html_chat_parser(path):
    with open(path, "r", encoding='utf-8') as chat:
        data = chat.read()
        soup = BeautifulSoup(data, 'html.parser')
        messages = soup.find_all(class_='clearfix')

        res = Chat()
        last_name = ""

        for msg in messages:

            if len(msg.select('.from_name')) > 0:
                last_name = msg.select('.from_name')[0].text.strip()
            user = User(last_name)

            if len(msg.select('.text')) > 0:
                text = msg.select('.text')[0].get_text(separator='\n').strip()
            else:
                continue
            date = msg.select('.date')[0]['title']
            date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S %Z%z")
            n_mes = Message(text, user, date)
            res.append(n_mes)

    return res


def parce_html_folder(path):
    res = Chat()
    filenames = os.listdir(path)
    files = []
    for filename in filenames:
        if filename.endswith('.html'):
            files.append(filename)  # add it to the list of folders
    files = sorted(files, key=extract_number)
    print(files)  # print the list of folders

    for file in files:
        if path.endswith('/'):
            ch = html_chat_parser(path + file)
        else:
            ch = html_chat_parser(path + '/' + file)
        res.merge(ch)
        print(f"{file} is done! {len(res.messages)} messages in total.")
    return res


def json_chat_parser(path):
    res = Chat()
    with open(path, "r", encoding='utf-8') as chat:
        chat = json.loads(chat.read())
        msgs = chat["messages"]

        for msg in msgs:
            if msg["type"] != "message":
                continue
            text = ""
            text_ent = msg["text_entities"]
            for txt in text_ent:
                text += txt["text"]

            user = User(msg["from"])
            date = msg["date"]
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
            n_mes = Message(text, user, date)
            res.append(n_mes)

    return res


def extract_number(s):
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    else:
        return 0
