"""Text simple conversion with bot
"""
import asyncio
import json
import requests
import re

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.updater import Updater


TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)


def wikiSearch(query, language):

    URL = 'http://%s.wikipedia.org/w/api.php?action=query&titles=Title&prop=links|extlinks' %language
    PARAMS = {
    'action':"query",
    'list':"search",
    'srsearch': query,
    'format':"json"}
    response = requests.get(url=URL, params=PARAMS)
    Data = response.json()
    results = ''
    summary = ''
    for item in Data['query']['search']:
        summary += remove_tags(item['snippet']) + '\n' + '\n'
        results += "http://%s.wikipedia.org/wiki/"%language + item['title'].replace(" ", "_") + '\n'
    
    return results





# A token you give from BotFather when you create your bot set below
updater = Updater(token="3c54b9b3f8a7698575c3e22872c4a0477ce1bb26",
                  loop=asyncio.get_event_loop())
bot = updater.dispatcher.bot
dispatcher = updater.dispatcher
language = ''
query = ''

def success(response, user_data):
    # Check if there is any user data or not
    if user_data:
        user_data = user_data['kwargs']
        user_peer = user_data["user_peer"]
        message = user_data["message"]
        print("message : " + message.text + "\nuser id : ", user_peer.peer_id)
    print("success : ", response)


def failure(response, user_data):
    print("user_data : ", user_data)
    print("failure : ", response)




@dispatcher.command_handler(["/start"])
# def conversation_starter(bot, update):
#     message = TextMessage("*Hi , come try a interesting message* \nplease tell me a *yes-no* question.")
#     user_peer = update.get_effective_user()
#     bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
#     dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), ask_question))


def ask_question(bot, update):
    user_peer = update.get_effective_user()
    # Set client message as general message of a template message
    general_message = TextMessage("زبان مورد نظر خود را انتخاب کنید:")
    # Create how many buttons you like with TemplateMessageButton class
    btn_list = [TemplateMessageButton(text="EN", value="en", action=0),
                TemplateMessageButton(text="FA", value="fa", action=0)]
    # Create a Template Message
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    bot.send_message(template_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update,
                                                       [MessageHandler(TemplateResponseFilter(keywords=["en"]),
                                                                       english_answer), MessageHandler(TemplateResponseFilter(keywords=["fa"]),
                                                                       persian_answer)])



def english_answer(bot, update):
    global language
    language = update.get_effective_message().text_message
    message = TextMessage("*Please enter your search query:*")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), english_conversion))


def persian_answer(bot, update):
    global language
    language = update.get_effective_message().text_message
    message = TextMessage("*عبارت مورد نظر خود را وارد کنید*")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(TextFilter(), persian_conversion))


def english_conversion(bot, update):
    user_peer = update.get_effective_user()
    query = update.get_effective_message().text


    if language == 'en' and len(wikiSearch(query, 'en')) != 0:
        message = TextMessage("*Your results are here:* \n" + wikiSearch(query, 'en'))
    else:
    	message = TextMessage("*Results not found*")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    # Finish conversation
    #dispatcher.english_conversion(update)

def persian_conversion(bot, update):
    user_peer = update.get_effective_user()
    query = update.get_effective_message().text


    if language == 'fa' and len(wikiSearch(query, 'fa')) != 0:
        message = TextMessage("*نتایج جست و جو:* \n" + wikiSearch(query, 'fa'))
    else:
    	message = TextMessage("*موردی یافت نشد.*")
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    # Finish conversation
    #dispatcher.persian_conversion(update)

updater.run()