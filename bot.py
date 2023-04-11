import telebot
from telebot.types import *

bot = telebot.TeleBot("5769907387:AAFy8gbt2j3VQ3poDRWZMhS46Gn21X2FW7o")

@bot.message_handler(commands =["start"])
def start_message(message):
	bot.send_message(message.chat.id, "Heya!")

print("Successful")
bot.infinity_polling()
