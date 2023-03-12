import os
import telebot
from bs4 import BeautifulSoup as bs
import requests
import json
from server import server
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

API_KEY = os.environ.get('API_KEY')
BASE = os.environ.get('BASE')
bot = telebot.TeleBot(API_KEY)
server()
file = []

def get_url(name):
    url = BASE + name.replace(" ", "%20")
    return url

def lyrics_scrape(name):
    #first page:
    time.sleep(0.01)
    r = requests.get(get_url(name), headers=headers)
    soup = bs(r.content, features='html.parser')
    data = soup.text
    parsed_json = json.loads(data)
    try:
        link = parsed_json['response']['sections'][1]['hits'][0]['result']['url']
    except:
        return "Sorry, no matches :)"
    info = parsed_json['response']['sections'][1]['hits'][0]['result']['full_title']
    file.append(info.replace('by','-') + ' Lyrics:\n\n')
        
    #second page (Entering the link):
    time.sleep(0.01)
    r1 = requests.get(link, headers=headers)
    soup1 = bs(r1.content, features='html.parser')
    lyrics_raw = soup1.find('div','Lyrics__Container-sc-1ynbvzw-6 YYrds')
    if lyrics_raw == None:
        lyrics_raw = soup1.find('div', 'LyricsPlaceholder__Message-uen8er-3 jlYyFx')

    #adding a new line for a new line.
    lyrics_fixed = str(lyrics_raw).replace('<br/>', '\n')

    convert = bs(lyrics_fixed, features='html.parser')
    lyrics = convert.text

    file.append(lyrics)

    lyricsfr = "".join(line for line in file)
    file.clear()
    return lyricsfr
        
def tbot():
    @bot.message_handler(commands=['start'])
    def start(message):
        smsg = "Hey, I am LyricsG Bot\nSend me the name of the song and I will get its lyrics for you <3\n(You can send with artist name for more accuarcy)."
        bot.reply_to(message, smsg)
        print("start")

    def ismsg(message):
        return True

    @bot.message_handler(func=ismsg)
    def reply(message):
        name = message.text
        print(name)
        time.sleep(0.01)
        lyrics = lyrics_scrape(name)
        bot.reply_to(message, lyrics)
        print("Done!")

    print('Bot is running...')
    bot.polling()


tbot()
