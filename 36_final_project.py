import telebot
from telebot import types

bot = telebot.TeleBot('7747821587:AAFVyH1JFPuC8e7lpBqBy-z5MyqSKHMLe_Y')

@bot.message_handler(commands=['start'])
def start(message):


bot.polling(none_stop=True)