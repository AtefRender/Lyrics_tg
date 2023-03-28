import os
import telebot
from telebot import types
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from server import server
import time

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

API_KEY = os.environ.get('API_KEY')
CHATID = os.environ.get('CHATID')
bot = telebot.TeleBot(API_KEY)

server()
file = []

def tbot():
    @bot.message_handler(commands=['start'])
    def start(message):
        smsg = "Bot moved to @LyricismRobot\nLink: https://t.me/LyricismRobot"
        bot.reply_to(message, smsg)
        print(str(message.chat.username) + " start")

    @bot.message_handler()
    def reply(message):
        name = message.text
        userId = message.chat.id
        nameUser = str(message.chat.first_name) + ' ' + str(message.chat.last_name)
        username = message.chat.username
        text = message.text
        date = datetime.now()
        data = f'User id: {userId}\nUsermae: {username}\nName: {nameUser}\nText: {text}\nDate: {date}'
        bot.send_message(chat_id=CHATID, text=data)
        smsg = "Bot moved to @LyricismRobot\nLink: https://t.me/LyricismRobot"
        bot.reply_to(message, smsg)
        
   
    print('Bot is running...')
    bot.infinity_polling()

tbot()
