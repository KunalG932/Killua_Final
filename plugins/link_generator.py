from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, OWNER_ID
from helper_func import encode, get_message_id
from database.database import is_admin

# Admin filter
class AdminRequired:
    def __init__(self):
        pass

    async def __call__(self, client, message):
        user_id = message.from_user.id
        is_admin_user, _ = await is_admin(user_id)
        if user_id == OWNER_ID or is_admin_user or user_id in ADMINS:
            return True
        else:
            await message.reply("❌ You don't have permission to use this command.")
            return False

# Create admin_required filter instance
admin_required = AdminRequired()



@Bot.on_message(filters.private & filters.command('batch') & admin_required)
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward The First Message From DB Channel (With Quotes)..\n\nOr Send The DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Forward The Last Message From DB Channel (With Quotes)..\n\nOr Send The DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here Is Your Link</b>\n\n{link}", quote=True, reply_markup=reply_markup)




@Bot.on_message(filters.private & filters.command('genlink') & admin_required)
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message From The DB Channel (With Quotes)..\n\nOr Send The DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here Is Your Link</b>\n\n{link}", quote=True, reply_markup=reply_markup)







# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Backup Channel @JishuBotz
# Developer @JishuDeveloper
