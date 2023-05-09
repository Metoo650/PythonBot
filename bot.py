import telebot
from telebot.types import *

bot = telebot.TeleBot("5769907387:AAF1QPdt8rgmFOLpM-PZaeooap_Vr27dJGI")

@bot.message_handler(commands =["start"])
def start_message(message):
	bot.send_message(message.chat.id, "Heya!")

print("Successful")
bot.infinity_polling()
