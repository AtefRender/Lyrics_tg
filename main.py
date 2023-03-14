import os
import telebot
from telebot import types
from bs4 import BeautifulSoup as bs
import requests
import json
from server import server
import time

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

API_KEY = os.environ.get('API_KEY')
BASE = os.environ.get('BASE')
bot = telebot.TeleBot(API_KEY)

server()
file = []

def get_url(name):
    url = BASE + name.replace(" ", "%20")
    return url

def first_page(name):
    #first page:
    time.sleep(0.01)
    r = requests.get(get_url(name), headers=headers)
    if r.status_code == 200:
        soup = bs(r.content, features='html.parser')
        data = soup.text
        parsed_json = json.loads(data)
        global searchq
        global links
        global photos
        searchq = []
        links = []
        photos = []
        global results_counter
        results_counter = len(parsed_json['response']['sections'][1]['hits'])
        print(results_counter)
        for x in range(results_counter):
            link = parsed_json['response']['sections'][1]['hits'][x]['result']['url']
            info = parsed_json['response']['sections'][1]['hits'][x]['result']['full_title']
            photo = parsed_json['response']['sections'][1]['hits'][x]['result']['song_art_image_url']
            links.append(link)
            searchq.append(info)
            photos.append(photo)

        if results_counter == 0:
            return "Sorry, no matches :)"
        
        print(searchq)
        
    else:
        print("Server error")
        return "Sorry, server error :)"

def second_page(link):
    #second page (Entering the link):
    time.sleep(0.01)
    r1 = requests.get(link, headers=headers)
    if r1.status_code == 200:
        soup1 = bs(r1.content, features='html.parser')

        #About the song:
        global about 
        try:
            about = soup1.find('div', 'SongDescription__Content-sc-615rvk-2 kRzyD').get_text()
            if about == None:
                about = 'Sorry, couldn\'t find data.'
        except:
            about = 'Sorry, couldn\'t find data.'

        #Album tracklist:
        global album 
        try:
            album = soup1.find('ol', 'AlbumTracklist__Container-sc-123giuo-0 kGJQLs')
            if album == None:
                album = 'Sorry, couldn\'t find data.'
            else:
                album_fixed = str(album).replace('</li>','\n')
                convert_album = bs(album_fixed, features='html.parser')
                album = convert_album.text
        except:
            album = 'Sorry, couldn\'t find data.'

        #Lyrics
        lyrics_raw = soup1.find('div','Lyrics__Container-sc-1ynbvzw-6 YYrds')
        if lyrics_raw == None:
            lyrics_raw = soup1.find('div', 'LyricsPlaceholder__Message-uen8er-3 jlYyFx')
        lyrics_fixed = str(lyrics_raw).replace('<br/>', '\n')
        convert = bs(lyrics_fixed, features='html.parser')
        lyrics = convert.text
        file.append(lyrics)

    else:
        print("Server error")
        return "Sorry, Server error :)"
        
def tbot():
    @bot.message_handler(commands=['start'])
    def start(message):
        smsg = "Hey, I am LyricsG Bot\nSend me the name of the song and I will get its lyrics for you <3\n(You can send with artist name for more accuarcy)."
        bot.reply_to(message, smsg)
        print(str(message.chat.username) + " start")

    @bot.message_handler()
    def reply(message):
        name = message.text
        print(str(message.chat.username) + ' - ' + name)
        first_page(name)

        #Serch kb:
        markup = types.InlineKeyboardMarkup()
        count = 0
        for value in searchq:
            markup.add(types.InlineKeyboardButton(text=value,callback_data='result'+str(count)))
            count += 1
        markup.add(types.InlineKeyboardButton(text='Close', callback_data='result_no'))
        #More info kb:
        global keyboard
        keyboard = types.InlineKeyboardMarkup()
        button0 = types.InlineKeyboardButton(text='About the song', callback_data='click0')
        button1 = types.InlineKeyboardButton(text='Album tracklist', callback_data='click1')
        button2 = types.InlineKeyboardButton(text='Done', callback_data='click2')
        keyboard.row(button0, button1, button2)
        if results_counter != 0:
            bot.reply_to(message, 'Choose your song:', reply_markup=markup)
        else:
            bot.reply_to(message, 'Sorry, no matches :)')


    @bot.callback_query_handler(func=lambda call: True)
    def callback_data(call):
        if call.message:
            if call.data == 'result_no':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            if call.data == 'result0':
                global lyricsfr
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                second_page(links[0])
                file.insert(0, searchq[0] + ' | Lyrics:\n\n')
                lyricsfr = "".join(line for line in file)
                file.clear()
                bot.send_photo(chat_id=call.message.chat.id, photo=photos[0])
                bot.send_message(chat_id=call.message.chat.id, text=lyricsfr, reply_markup=keyboard)
            if call.data == 'result1':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                second_page(links[1])
                file.insert(0, searchq[1] + ' | Lyrics:\n\n')
                lyricsfr = "".join(line for line in file)
                file.clear()
                bot.send_photo(chat_id=call.message.chat.id, photo=photos[1])
                bot.send_message(chat_id=call.message.chat.id, text=lyricsfr, reply_markup=keyboard)
            if call.data == 'result2':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                second_page(links[2])
                file.insert(0, searchq[2] + ' | Lyrics:\n\n')
                lyricsfr = "".join(line for line in file)
                file.clear()
                bot.send_photo(chat_id=call.message.chat.id, photo=photos[2])
                bot.send_message(chat_id=call.message.chat.id, text=lyricsfr, reply_markup=keyboard)
            if call.data == 'result3':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                second_page(links[2])
                file.insert(0, searchq[3] + ' | Lyrics:\n\n')
                lyricsfr = "".join(line for line in file)
                file.clear()
                bot.send_photo(chat_id=call.message.chat.id, photo=photos[2])
                bot.send_message(chat_id=call.message.chat.id, text=lyricsfr, reply_markup=keyboard)
            if call.data == 'result4':
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                second_page(links[4])
                file.insert(0, searchq[4] + ' | Lyrics:\n\n')
                lyricsfr = "".join(line for line in file)
                file.clear()
                bot.send_photo(chat_id=call.message.chat.id, photo=photos[4])
                bot.send_message(chat_id=call.message.chat.id, text=lyricsfr, reply_markup=keyboard)
            
            if call.data == 'click0':
                bot.send_message(chat_id=call.message.chat.id, text='About the song:\n' + about)
            if call.data == 'click1':
                bot.send_message(chat_id=call.message.chat.id, text='Album tracklist:\n' + album)
            if call.data == 'click2':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lyricsfr)

    print('Bot is running...')
    bot.infinity_polling()

tbot()