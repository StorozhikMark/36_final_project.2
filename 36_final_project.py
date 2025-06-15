import telebot

API_TOKEN = open('token.txt').readline()

bot = telebot.TeleBot(API_TOKEN)

status = open('Состояние.txt').readlines()
status = [int(status[0]), int(status[1]), int(status[2])]

@bot.message_handler(commands=['start'])
def start(message):
    global status
    bot.send_message(message.chat.id, 'Привет! Я бот "Тамагочи". У тебя есть питомец. Ты можешь посмотреть его состояние, если наберёшь команду /status. Ты можешь покормить питомца, поиграть с ним и вылечить с помощью команд /feed, /play, /heal')
    status[0] += 1
    status[1] -= 1
    status[2] -= 1
    with open('Состояние.txt', 'w') as file:
        file.write(f'{status[0]}\n{status[1]}\n{status[2]}')

@bot.message_handler(commands=['status'])
def send_status(message):
    global status
    bot.send_message(message.chat.id, f'Голод - {status[0]}\nНастроение - {status[1]}\nЗдоровье - {status[2]}')
    status[0] += 1
    status[1] -= 1
    status[2] -= 1
    with open('Состояние.txt', 'w') as file:
        file.write(f'{status[0]}\n{status[1]}\n{status[2]}' )

@bot.message_handler(commands=['feed'])
def feed(message):
    global status
    status[0] = 0
    bot.send_message(message.chat.id, f'Вы покормили питомца! Голод - {status[0]}')
    status[1] -= 1
    status[2] -= 1
    with open('Состояние.txt', 'w') as file:
        file.write(f'{status[0]}\n{status[1]}\n{status[2]}')

@bot.message_handler(commands=['play'])
def play(message):
    global status
    status[1] = 100
    bot.send_message(message.chat.id, f'Вы поиграли с питомцем! Настроение - {status[1]}')
    status[0] += 1
    status[2] -= 1
    with open('Состояние.txt', 'w') as file:
        file.write(f'{status[0]}\n{status[1]}\n{status[2]}')

@bot.message_handler(commands=['heal'])
def heal(message):
    global status
    status[2] = 100
    bot.send_message(message.chat.id, f'Вы вылечили питомца! Здоровье - {status[2]}')
    status[0] += 1
    status[1] -= 1
    with open('Состояние.txt', 'w') as file:
        file.write(f'{status[0]}\n{status[1]}\n{status[2]}')

bot.polling(none_stop=True)



