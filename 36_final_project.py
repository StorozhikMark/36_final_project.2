import telebot
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

API_TOKEN = open('token.txt').readline()

bot = telebot.TeleBot(API_TOKEN)

def load_status():
    with open('Состояние.txt', 'r') as file:
        status = file.readlines()
        status1 = {}
    for i in range(0, len(status), 4):
        status1[status[i]] = [int(status[i+1]), int(status[i+2]), int(status[i+3])]
    return status1

status = load_status()

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
    scheduler.add_job(decrease_status, 'interval', seconds=1)

@bot.message_handler(commands=['status'])
def send_status(message):
    global status
    chat_id = message.chat.id
    bot.send_message(message.chat.id, f'Голод - {status[message.chat.id][0]}\nНастроение - {status[message.chat.id][1]}\nЗдоровье - {status[message.chat.id][2]}')
    save_status(status, message.chat.id)

@bot.message_handler(commands=['feed'])
def feed(message):
    global status
    chat_id = message.chat.id
    bot.send_message(message.chat.id, f'Вы покормили питомца! Голод - {status[message.chat.id][0]}')
    save_status(status, message.chat.id)

@bot.message_handler(commands=['play'])
def play(message):
    global status
    chat_id = message.chat.id
    bot.send_message(message.chat.id, f'Вы поиграли с питомцем! Настроение - {status[message.chat.id][1]}')
    save_status(status, message.chat.id)

@bot.message_handler(commands=['heal'])
def heal(message):
    global status
    chat_id = message.chat.id
    bot.send_message(message.chat.id, f'Вы вылечили питомца! Здоровье - {status[message.chat.id][2]}')
    save_status(status, message.chat.id)

def decrease_status():
    status = load_status()
    status[chat_id][0] = max(0, status[chat_id][0] + 5)
    status[chat_id][1] = max(0, status[chat_id][1] - 5)
    status[chat_id][2] = max(0, status[chat_id][2] - 5)  # Уменьшаем здоровье, но не ниже 0
    save_status(status, chat_id)

bot.polling(none_stop=True)