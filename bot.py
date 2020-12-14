import sqlite3
import telebot
from telebot import *

bot = telebot.TeleBot("907171461:AAHpZEmfC3dVCNYC-G7N11zhiQMib7YwxVY", parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add('Скинь документ')
	bot.reply_to(message, 'Введите слово или словосочетание для поиска. Для получения документа с вопросами и ответами нажми "Скинь документ"', reply_markup=markup)
	print(f'{message.chat.id}, {message.from_user.username} -> start')
	if message.chat.id != 888833912:
		bot.send_message(888833912, f'{message.chat.id}, {message.from_user.username} -> start')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	
	cid = message.chat.id

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add('Скинь документ')

	if message.text == 'Скинь документ':
		doc = open('psih.docx', 'rb')
		print(f'{cid}, {message.from_user.username} -> document')
		bot.send_document(cid, doc, reply_markup=markup)
		if cid != 888833912:
			bot.send_message(888833912, f'{cid}, {message.from_user.username} -> document')

	else:
		con = sqlite3.connect('bot_db.sqlite3')
		cur = con.cursor()
		for row in cur.execute('SELECT * FROM answers'):
			if (message.text in str(row[1])) or (message.text.lower() in str(row[1])) or (message.text.upper() in str(row[1])) or (message.text.capitalize() in str(row[1])):
				bot.send_message(cid, f'{row[1]}\n\n{row[2]}', reply_markup=markup)
				print(f'{cid}, {message.from_user.username}: {row[1]} --> {row[2]}')
				if cid != 888833912:
					bot.send_message(888833912, f'{cid}, {message.from_user.username}: {row[1]} --> {row[2]}')
bot.polling()
