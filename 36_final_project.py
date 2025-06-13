import telebot
from telebot import types

bot = telebot.TeleBot('7747821587:AAFVyH1JFPuC8e7lpBqBy-z5MyqSKHMLe_Y')

hunger = 0
mood = 100
health = 100

@bot.message_handler(commands=['start'])
def start(message):
    global hunger, mood, health
    bot.send_message(message.chat.id, 'Привет! Я бот "Тамагочи". У тебя есть питомец. Ты можешь посмотреть его состояние, если наберёшь команду /status. Ты можешь покормить питомца, поиграть с ним и вылечить с помощью команд /feed, /play, /heal')
    hunger += 1
    mood -= 1
    health -= 1

@bot.message_handler(commands=['status'])
def status(message):
    global hunger, mood, health
    bot.send_message(message.chat.id, f'Голод - {hunger}\nНастроение - {mood}\nЗдоровье - {health}')
    hunger += 1
    mood -= 1
    health -= 1

@bot.message_handler(commands=['feed'])
def feed(message):
    global hunger, mood, health
    hunger = 0
    bot.send_message(message.chat.id, f'Вы покормили питомца! Голод - {hunger}')
    mood -= 1
    health -= 1

@bot.message_handler(commands=['play'])
def play(message):
    global hunger, mood, health
    mood = 100
    bot.send_message(message.chat.id, f'Вы поиграли с питомцем! Настроение - {mood}')
    hunger += 1
    health -= 1

@bot.message_handler(commands=['heal'])
def heal(message):
    global hunger, mood, health
    health = 100
    bot.send_message(message.chat.id, f'Вы вылечили питомца! Здоровье - {health}')
    hunger += 1
    mood -= 1


bot.polling(none_stop=True)