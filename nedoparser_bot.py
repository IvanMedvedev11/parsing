import telebot
import pandas as pd
from conf import TOKEN
import requests
from bs4 import BeautifulSoup
import lxml
cnt = 0
soup = ''
teg = ''
class_ = ''
res = ''
title = ''
data = []
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, я бот парсер. Для того чтобы запарсить сайт, введите ссылку на него, а также тег и класс объектов, которые нужно получить")
@bot.message_handler(content_types=["text"])
def parsing(message):
    global cnt
    global soup
    global teg
    global class_
    global data
    global res
    global title
    if cnt == 0:
        url = message.text
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        bot.send_message(message.chat.id, "Отлично, теперь введите тег")
        cnt+=1
    elif cnt == 1:
        teg = message.text
        bot.send_message(message.chat.id, "Теперь введите класс(или 'нет', если не нужно)")
        cnt+=1
    elif cnt == 2:
        class_ = message.text
        if class_.lower() == 'нет':
            res = soup.findAll(teg)
            print(res)
            cnt+=1
        else:
            res = soup.findAll(teg, class_=class_)
            print(res)
            cnt+=1
        bot.send_message(message.chat.id, "Теперь введи название колонки")
    elif cnt == 3:
        cnt = 0
        title = message.text
        for object in res:
            data.append(object.text.strip())
        df = pd.DataFrame(data, columns=[title])
        df.to_excel('parse.xlsx', index=False)
        with open('parse.xlsx', 'rb') as f:
            file = f.read()
        bot.send_document(message.chat.id,file, visible_file_name="parse.xlsx")
        data = []
bot.infinity_polling()
