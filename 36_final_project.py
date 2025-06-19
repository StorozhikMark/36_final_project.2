import telebot
from apscheduler.schedulers.background import BackgroundScheduler
import os
import dotenv

dotenv.load_dotenv()

scheduler = BackgroundScheduler()
scheduler.start()

API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def load_status():
    with open('Состояние.txt', 'r') as file:
        status = file.readlines()
        status1 = {}
    for i in range(0, len(status), 4):
        status[i] = int(status[i])
        status1[status[i]] = [int(status[i+1]), int(status[i+2]), int(status[i+3])]
    # print(status1)
    return status1

def decrease_status():
    status = load_status()
    status[chat_id][0] = min(100, status[chat_id][0] + 5)
    status[chat_id][1] = max(0, status[chat_id][1] - 5)
    status[chat_id][2] = max(0, status[chat_id][2] - 5)  # Уменьшаем здоровье, но не ниже 0
    save_status(status, chat_id)

status = load_status()
scheduler.add_job(decrease_status, 'interval', seconds=3)

def save_status(status, chat_id):
    with open('Состояние.txt', 'w') as file:
        file.write(f'{chat_id}\n{status[chat_id][0]}\n{status[chat_id][1]}\n{status[chat_id][2]}')

chat_id = ''

@bot.message_handler(commands=['start'])
def start(message):
    global status
    global chat_id
    chat_id = message.chat.id
    status[message.chat.id] = [0, 100, 100]
    save_status(status, message.chat.id)
    bot.send_message(message.chat.id, 'Привет! Я бот "Тамагочи". У тебя есть питомец. Ты можешь посмотреть его состояние, если наберёшь команду /status. Ты можешь покормить питомца, поиграть с ним и вылечить с помощью команд /feed, /play, /heal')

@bot.message_handler(commands=['status'])
def send_status(message):
    status = load_status()
    if status[message.chat.id][0] == 100 or status[message.chat.id][2] == 0:
        img = open('images/dead.jpg', 'rb')
    elif status[message.chat.id][0] > 50 or status[message.chat.id][2] < 50:
        img = open('images/sad.png', 'rb')
    else:
        img = open('images/happy.png', 'rb')
    bot.send_photo(message.chat.id, img, caption=f'Голод - {status[message.chat.id][0]}\nНастроение - {status[message.chat.id][1]}\nЗдоровье - {status[message.chat.id][2]}')

@bot.message_handler(commands=['feed'])
def feed(message):
    status = load_status()
    status[message.chat.id][0] = 0
    bot.send_message(message.chat.id, f'Ты покормил питомца! Голод - {status[message.chat.id][0]}')
    save_status(status, message.chat.id)

@bot.message_handler(commands=['play'])
def play(message):
    status = load_status()
    status[message.chat.id][1] = 100
    bot.send_message(message.chat.id, f'Ты поиграл с питомцем! Настроение - {status[message.chat.id][1]}')
    save_status(status, message.chat.id)

@bot.message_handler(commands=['heal'])
def heal(message):
    status = load_status()
    status[message.chat.id][2] = 100
    bot.send_message(message.chat.id, f'Ты вылечил питомца! Здоровье - {status[message.chat.id][2]}')
    save_status(status, message.chat.id)


bot.polling(none_stop=True)