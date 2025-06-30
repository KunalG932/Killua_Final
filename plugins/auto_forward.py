from pyrogram import Client, filters
from pyrogram.types import Message
import re
from database.database import is_admin
from config import OWNER_ID, ADMINS

# Admin filter
class A:
    async def __call__(self, c, m):
        u = m.from_user.id
        ok, _ = await is_admin(u)
        if u == OWNER_ID or ok or u in ADMINS:
            return True
        await m.reply("❌ You can't use this.")
        return False

a = A()

# Default for auto-forward
SRC = -1002053608688  # Update this
DST = -1002773214491  # Update this

# Store per-user config temporarily in memory (you can replace with DB)
cfg = {}

# ========== Auto Forwarding New Posts ==========
@Client.on_message(filters.channel & filters.chat(SRC))
async def fwd(c, m: Message):
    try:
        await m.copy(DST)
    except Exception as e:
        print(f"Error forwarding {m.id}: {e}")

# ========== Command to Set Manual Source & Destination ==========
@Client.on_message(filters.command("set_forward_config") & filters.private & a)
async def set_cfg(c, m: Message):
    x = m.text.split()
    if len(x) != 3:
        return await m.reply("Usage: `/set_forward_config source_id destination_id`", quote=True)
    try:
        s = int(x[1])
        d = int(x[2])
        cfg[m.from_user.id] = {"src": s, "dst": d}
        await m.reply(f"✅ Config set:\nSource: `{s}`\nDestination: `{d}`")
    except Exception as e:
        await m.reply(f"⚠️ Error: {e}")

# ========== Manual Command to Forward Old Posts ==========
@Client.on_message(filters.command("forward_old") & filters.private & a)
async def fwd_old(c, m: Message):
    x = m.text.split()
    if len(x) < 3:
        return await m.reply("Usage:\n`/forward_old start_id end_id`\nor\n`/forward_old https://t.me/c/ID/100 https://t.me/c/ID/110`", quote=True)
    def get_id(v):
        m_ = re.search(r'/([0-9]+)$', v)
        return int(m_.group(1)) if m_ else int(v)
    try:
        s = get_id(x[1])
        e = get_id(x[2])
        if s > e:
            return await m.reply("⚠️ Start ID must be <= End ID.")
        u = m.from_user.id
        c_ = cfg.get(u, {"src": SRC, "dst": DST})
        src = c_["src"]
        dst = c_["dst"]
        await m.reply(f"🔄 Forwarding `{s}` to `{e}`\nFrom `{src}` → `{dst}`")
        for i in range(s, e + 1):
            try:
                msg = await c.get_messages(src, i)
                await msg.copy(dst)
            except Exception as ex:
                print(f"Failed to forward {i}: {ex}")
        await m.reply("✅ Done.")
    except Exception as e:
        await m.reply(f"⚠️ Error: {e}")

