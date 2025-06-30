from aiohttp import web
from plugins import web_server

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from config import API_HASH, ADMINS, API_ID, LOGGER, BOT_TOKEN, TG_BOT_WORKERS, CHANNEL_ID, PORT, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, REQUEST_CHANNEL_1, REQUEST_CHANNEL_2
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009999999999



class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        
        if REQUEST_CHANNEL_1:
            try:
                link_a = (await self.create_chat_invite_link(chat_id=REQUEST_CHANNEL_1, creates_join_request=True)).invite_link 
                self.link_one = link_a                                     
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the REQUEST_CHANNEL_1 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {REQUEST_CHANNEL_1}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/Manga_Campus_Chat for support")
                sys.exit()
        if REQUEST_CHANNEL_2:
            try:
                link_b = (await self.create_chat_invite_link(chat_id=REQUEST_CHANNEL_2, creates_join_request=True)).invite_link 
                self.link_two = link_b                                  
            except Exception as b:
                self.LOGGER(__name__).warning(b)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the REQUEST_CHANNEL_2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {REQUEST_CHANNEL_2}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/Manga_Campus_Chat for support")
                sys.exit()

        # Primary force-subscription channel
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot Can't Export Invite link from primary Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double Check The FORCE_SUB_CHANNEL Value And Make Sure Bot Is Admin In Channel With Invite Users Via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. https://t.me/Manga_Campus_Chat For Support")
                sys.exit()
        # Secondary force-subscription channel
        if FORCE_SUB_CHANNEL2:
            try:
                link2 = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link2:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link2 = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link2
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot Can't Export Invite link from secondary Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double Check The FORCE_SUB_CHANNEL2 Value And Make Sure Bot Is Admin In Channel With Invite Users Via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL2}")
                self.LOGGER(__name__).info("\nBot Stopped. https://t.me/Manga_Campus_Chat For Support")
                sys.exit()


        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Hey ")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure Bot Is Admin In DB Channel, And Double Check The CHANNEL_ID Value, Current Value: {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/Manga_Campus_Chat For Support")
            sys.exit()

        
        self.LOGGER(__name__).info(f"Bot Running...!\n\nCreated By \nhttps://t.me/Aaru_2074")
        self.LOGGER(__name__).info(f"""Aaru""")
        self.username = usr_bot_me.username
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot Stopped...")
