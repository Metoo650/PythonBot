from pyrogram import Client, filters
from pyromod import listen
import datetime
from pyrogram.types import *
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb+srv://really651:K4vSnRMEsZhqsTqS@cluster0.pxc2foz.mongodb.net/?retryWrites=true&w=majority")

db = client["RenamerDB"]
collection = db["renamerbot"]

app = Client("uploaderv5bot", api_id=11855414,api_hash="71449899c824b5bc9a91d8a52b20c5f3",bot_token="5769907387:AAF1QPdt8rgmFOLpM-PZaeooap_Vr27dJGI")

admin = [1365625365, 1170583016]

@app.on_message(filters.command("start"))
async def strf(_, message):
	welcomemsg = f"Hey {message.from_user.mention}👋,\n\nThis bot can help you to rename files easily🕹\n🚀Just send me your files..."
	chat_id = message.chat.id 
	now = datetime.datetime.now()
	user = collection.find_one({'user_id': chat_id})
	if user:
		await message.reply(welcomemsg, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="✨Join My Updates✨", url="t.me/mt_projectz")]]))
	else:
		collection.insert_one({"user_id": message.chat.id, "premium": False, "banned": False})
		await message.reply(welcomemsg, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="✨Join My Updates✨", url="t.me/mt_projectz")]]))

async def download_progress(current, total):
    percent = current * 100 / total    
    current_mb = current / (1024 * 1024)
    total_mb = total / (1024 * 1024)
    await msg.edit(f"Download info: \nDownloaded:  {current_mb:.2f} MB ■ {total_mb:.2f} MB, ({percent:.2f}%)")

async def rename(_, message):
    global msg
    now = datetime.datetime.now()
    name = await message.chat.ask("📃Send me your new file name(No Extension Required):) or /cancel", reply_to_message_id = message.id)
    try:
    	if name.text == "/cancel":
    		return await message.reply("Cancelled")
    	else:
    		if len(name.text) > 100:
    			return await message.reply("⚠️The file name must be less than 100 characters:)")
    		else:
    			collection.update_one({"user_id": message.chat.id}, {"$set": {"bonus_time": now}})
    			msg = await message.reply("Processing your request...", reply_to_message_id = name.id)
    			file_name = message.document.file_name
    			file_extension = file_name.split(".")[-1] 
    			new_file_name = f"{name.text}." + file_extension
    			file_path = await app.download_media(message, progress=download_progress)
    			nwmsg = await msg.edit(f"🔄Renaming your file to {name.text}.....")
    			async def progress(current, total):
    				percent = current * 100 / total
    				current_mb = current / (1024 * 1024)
    				total_mb = total / (1024 * 1024)
    				await nwmsg.edit(f"Uploading info: \nUploaded  {current_mb:.2f} MB ■ {total_mb:.2f} MB, ({percent:.2f}%)")    			
    			await app.send_document(message.chat.id, file_path, file_name=new_file_name, reply_to_message_id=nwmsg.id, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="🗃Join My Updates🗃", url="t.me/mt_projectz")]]), progress= progress) 
    except Exception as e:
    	print(e)
    	await message.reply("⚠️Please Send me your new filename:) Try Again!")

async def rename_audio(_, message):
    global msg
    now = datetime.datetime.now()
    name = await message.chat.ask("📃Send me your new file name(No Extension Required):) or /cancel", reply_to_message_id = message.id)
    try:
    	if name.text == "/cancel":
    		return await message.reply("Cancelled")
    	else:
    		if len(name.text) > 100:
    			return await message.reply("⚠️The audio name must be less than 100 characters:)")
    		else:
    			collection.update_one({"user_id": message.chat.id}, {"$set": {"bonus_time": now}})
    			msg = await message.reply("Processing your request...", reply_to_message_id = name.id)
    			file_name = message.audio.file_name
    			file_extension = file_name.split(".")[-1] 
    			new_file_name = f"{name.text}." + file_extension
    			file_path = await app.download_media(message, progress=download_progress)
    			nwmsg = await msg.edit(f"🔄Renaming your file to {name.text}.....")
    			async def progress(current, total):
    				percent = current * 100 / total
    				current_mb = current / (1024 * 1024)
    				total_mb = total / (1024 * 1024)
    				await nwmsg.edit(f"Uploading info: \nUploaded  {current_mb:.2f} MB ■ {total_mb:.2f} MB, ({percent:.2f}%)")
    			await app.send_audio(message.chat.id, file_path, file_name=new_file_name, reply_to_message_id=nwmsg.id, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="🗃Join My Updates🗃", url="t.me/mt_projectz")]]), progress = progress)    			
    except:
    	await message.reply("⚠️Please Send me your new filename:) Try Again!")


channels = ["@mt_projectz"]

async def check_sub(_, message):
	try:
		for channel in channels:
			user = await app.get_chat_member(channel, message.chat.id)
			if user.status == "left":
				return False
		return True
	except:
			return False

@app.on_message(filters.audio)
async def renamer_audio(client, message):
	user = collection.find_one({"user_id": message.chat.id})
	if user["banned"] == True:
		return await message.reply("⚠️You have been banned because you broke the rules⚠️")
	else:
		pass
	sub = await check_sub(client, message)
	if sub == False:
		return await message.reply(f"⚠️Dear {message.from_user.mention} In order to use this bot you must be a member of our channel\n@MT_Projectz", reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="✨Join My Updates✨", url="t.me/mt_projectz")]]))
	else:
		pass
	chat_id = message.chat.id 
	now = datetime.datetime.now()
	if user and "bonus_time" in user:
		bonus_time = user['bonus_time']
		if now - bonus_time < datetime.timedelta(minutes=5):
			return await message.reply(f"Flooding: You have to wait 5 minutes before renaming another file:)\nYou can rename after 5 minutes✨")	
		else:
			size = message.audio.file_size / 1024 / 1024
			if size > 1000:
				return await message.reply("🤨Cannot rename a file larger than 1000MB")
			else:
				await rename_audio(client, message)
	else:
		await rename_audio(client, message)		

@app.on_message(filters.document)
async def rename_file(client, message):
	user = collection.find_one({"user_id": message.chat.id})
	if user["banned"] == True:
		return await message.reply("⚠️You have been banned because you broke the rules⚠️")
	else:
		pass
	sub = await check_sub(client, message)
	if sub == False:
		return await message.reply(f"⚠️Dear {message.from_user.mention} In order to use this bot you must be a member of our channel\n@MT_Projectz", reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="✨Join My Updates✨", url="t.me/mt_projectz")]]))
	else:
		pass
	await app.copy_message("@loggerpatcher", message.chat.id, message.id, caption=f"Name: {message.from_user.first_name}\nUserID: {message.from_user.id}")	
	chat_id = message.chat.id 
	now = datetime.datetime.now()
	if user and "bonus_time" in user:
		bonus_time = user["bonus_time"]
		if now - bonus_time < datetime.timedelta(minutes=5):
			return await message.reply(f"Flooding: You have to wait 5 minutes before renaming another file:)\nYou can rename after 5 minutes✨")		
		else:
			size = message.document.file_size / 1024 / 1024
			if size > 1500:
				return await message.reply("🤨Cannot rename a file larger than 1000MB")
			else:
				await rename(client, message)
	else:
		await rename(client, message)
    
    
print("Successful")
app.run()
