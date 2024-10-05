import config
import telebot
from telebot import types
from data.repository import DbRepository

# db = Database('db.db')
bot = telebot.TeleBot(config.TOKEN)
db = DbRepository(config.DB_URL)


@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    bot.send_message(
        message.chat.id, f'Привет, {message.from_user.first_name}, добро пожаловать в анонимный чат! нажми на кнопку найти собеседника', reply_markup=markup)

    
@bot.message_handler(commands=['stop'])
def stop_command(message):
    active_chat = db.get_active_chat(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)
    if active_chat:
        db.delete_chat(active_chat)
        if str(message.chat.id) == active_chat.chat_one: 
            bot.send_message(active_chat.chat_two, 'Собеседник завершил чат', reply_markup=markup)
            bot.send_message(active_chat.chat_one, 'Вы завершили чат', reply_markup=markup)
        else: 
            bot.send_message(active_chat.chat_one, 'Собеседник завершил чат', reply_markup=markup)
            bot.send_message(active_chat.chat_two, 'Вы завершили чат', reply_markup=markup)
    else:
        if (db.get_chat_from_chat_id(message.chat.id)):
            stop_search(message)
        else: 
            bot.send_message(message.chat.id, 'Вы не начали чат', reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Меню', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Поиск собеседника')
def search_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Остановить поиск')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Ищем...', reply_markup=markup)
    
    chat_two = db.get_chat()
    
    if not chat_two:
        db.add_queue(message.chat.id)
    else: 
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Собеседник найден', reply_markup=markup)
        bot.send_message(chat_two.chat_id, 'Собеседник найден', reply_markup=markup)
        db.create_chat(message.chat.id, chat_two.chat_id)
        db.delete_queue(chat_two)

@bot.message_handler(func=lambda message: message.text == 'Остановить поиск')
def stop_search(message):
    db.delete_queue(message.chat.id)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Поиск остановлен', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    active_chat = db.get_active_chat(message.chat.id)
    if active_chat: 
        markup = types.ReplyKeyboardRemove()
        if str(message.chat.id) == active_chat.chat_one: 
            bot.send_message(active_chat.chat_two, message.text, reply_markup=markup)
        else: 
            bot.send_message(active_chat.chat_one, message.text, reply_markup=markup)
    else: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Поиск собеседника')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Найдите собеседника для общения', reply_markup=markup)

bot.polling(none_stop=True)
