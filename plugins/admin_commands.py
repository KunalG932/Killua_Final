import os
from pyrogram import Client, filters
from pyrogram.types import Message
from database.database import add_admin, remove_admin, list_admins, is_admin
from config import OWNER_ID, ADMINS

class Admin:
    async def __call__(self, c, m):
        u = m.from_user.id
        ok, _ = await is_admin(u)
        if u == OWNER_ID or ok or u in ADMINS:
            return True
        await m.reply("❌ You can't use this.")
        return False

a = Admin()

@Client.on_message(filters.command("addadmin") & a)
async def add(c, m: Message):
    if not m.reply_to_message and len(m.command) < 2:
        await m.reply("Reply to a user or give user ID.")
        return
    try:
        u = m.reply_to_message.from_user.id if m.reply_to_message else int(m.command[1])
        user = await c.get_users(u)
        s = m.command[2].lower() if len(m.command) > 2 else 'admin'
        ok, msg = await add_admin(u, s)
        if ok:
            await m.reply(f"✅ Added {user.mention} as {s}")
            try:
                await c.send_message(u, f"🎉 You're now admin: {s}")
            except:
                pass
        else:
            await m.reply(f"❌ {msg}")
    except (IndexError, ValueError):
        await m.reply("❌ Invalid user ID.")
    except Exception as e:
        await m.reply(f"❌ Error: {e}")

@Client.on_message(filters.command("removeadmin") & a)
async def rem(c, m: Message):
    if not m.reply_to_message and len(m.command) < 2:
        await m.reply("Reply to a user or give user ID.")
        return
    try:
        u = m.reply_to_message.from_user.id if m.reply_to_message else int(m.command[1])
        user = await c.get_users(u)
        ok, msg = await remove_admin(u)
        if ok:
            await m.reply(f"✅ Removed {user.mention} from admins.")
            try:
                await c.send_message(u, "ℹ️ You're no longer admin.")
            except:
                pass
        else:
            await m.reply(f"❌ {msg}")
    except (IndexError, ValueError):
        await m.reply("❌ Invalid user ID.")
    except Exception as e:
        await m.reply(f"❌ Error: {e}")

@Client.on_message(filters.command("listadmins") & a)
async def show(c, m: Message):
    try:
        x = await list_admins()
        if not x:
            await m.reply("No admins.")
            return
        out = []
        for i, s in x:
            try:
                u = await c.get_users(i)
                n = f"{u.first_name} {u.last_name or ''}".strip()
                out.append(f"• {n} (@{u.username or 'N/A'}) - {s}")
            except:
                out.append(f"• ID: {i} - {s}")
        await m.reply("👑 **Admin List**\n\n" + "\n".join(out))
    except Exception as e:
        await m.reply(f"❌ Error: {e}")

@Client.on_message(filters.command("myadmin") & filters.private)
async def mine(c, m: Message):
    u = m.from_user.id
    ok, s = await is_admin(u)
    if ok:
        await m.reply(f"🛡️ Your admin status: **{s}**")
    else:
        await m.reply("❌ You're not admin.")
