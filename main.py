#import os
import telebot
from bs4 import BeautifulSoup as bs
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }

#API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot('6294630132:AAHRNORsY4Of-0BlappS05pT64WhoK_GyPs')

file = []
def get_url(name):
    base = "https://genius.com/api/search/multi?per_page=5&q="
    url = base + name.replace(" ", "%20")
    return url

def lyrics_scrape(name):
    with requests.Session() as s:
        #first page:
        r = requests.get(get_url(name), headers=headers)
        soup = bs(r.content, features='lxml')
        data = soup.text
        parsed_json = json.loads(data)
        link = parsed_json['response']['sections'][1]['hits'][0]['result']['url']
        info = parsed_json['response']['sections'][1]['hits'][0]['result']['full_title']
        file.append(info.replace('by','-') + ' Lyrics:\n\n')
        
        #second page (Entering the link):
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
        smsg = "Hey, I am a lyrics bot\nSend me the name of the song and I will get its lyrics for you <3\n(You can send with artist name for more accuarcy)."
        bot.reply_to(message, smsg)
        print("start")

    def ismsg(message):
        return True

    @bot.message_handler(func=ismsg)
    def reply(message):
        name = message.text
        print(name)
        lyrics = lyrics_scrape(name)
        bot.reply_to(message, lyrics)
        print(lyrics)

    print('Bot is running...')
    bot.polling()


tbot()
