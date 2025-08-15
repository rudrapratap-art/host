# File: /pyrogram-bot-render/pyrogram-bot-render/src/newfile.py
import os
import asyncio
import io
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp
import logging

def human_readable_size(size):
    if not size:
        return "unknown"
    size = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024.0:
            return f"{size:.2f}{unit}"
        size /= 1024.0
    return f"{size:.2f}PB"

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not API_ID or not API_HASH:
    raise RuntimeError("API_ID and API_HASH must be set in the environment")

try:
    api_id = int(API_ID)
except ValueError:
    raise RuntimeError("API_ID must be an integer")

if BOT_TOKEN:
    app = Client("bot", api_id=api_id, api_hash=API_HASH, bot_token=BOT_TOKEN)
else:
    app = Client("user", api_id=api_id, api_hash=API_HASH)

def do_extract(url):
    opts = {
        "quiet": True,
        "nocheckcertificate": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if isinstance(info, dict) and info.get("entries"):
            entries = info.get("entries")
            if entries:
                return entries[0]
        return info

@app.on_message(filters.private & filters.text & ~filters.command(["start"]))
async def handle_link(client: Client, m: Message):
    url = m.text.strip()
    status_msg = await m.reply_text("🔍 Extracting downloadable links…")

    try:
        info = await asyncio.to_thread(do_extract, url)

        title = info.get("title", "video")
        formats = info.get("formats") or []

        def fmt_score(f):
            score = 0
            if f.get("vcodec") != "none" and f.get("acodec") != "none":
                score += 1000
            height = f.get("height") or 0
            tbr = f.get("tbr") or 0
            score += height * 10 + int(tbr or 0)
            return score

        formats_with_url = [f for f in formats if f.get("url")]
        if not formats_with_url:
            direct = info.get("url")
            if direct:
                await client.edit_message_text(
                    chat_id=status_msg.chat.id,
                    message_id=status_msg.id,
                    text=f"🔗 Direct URL for {title}:\n{direct}"
                )
                return
            else:
                await client.edit_message_text(
                    chat_id=status_msg.chat.id,
                    message_id=status_msg.id,
                    text="No downloadable links found."
                )
                return

        top_formats = sorted(formats_with_url, key=fmt_score, reverse=True)[:8]

        lines = [f"🎬 {title}\n\nAvailable direct links:"]
        for f in top_formats:
            ext = f.get("ext", "bin")
            note = f.get("format_note") or f.get("format") or ""
            res = f"{f.get('height')}p" if f.get("height") else ""
            raw_size = f.get("filesize") if f.get("filesize") is not None else f.get("filesize_approx")
            if raw_size is not None:
                size_str = human_readable_size(raw_size)
                size_display = f"— {size_str}"
            else:
                size_display = "— size unknown"
            lines.append(f"• {ext} {res} {note} {size_display}\n{f['url']}")

        output_message = "\n\n".join(lines)

        if len(output_message) > 4000:
            bio = io.BytesIO(output_message.encode("utf-8"))
            bio.name = "links.txt"
            await client.send_document(chat_id=m.chat.id, document=bio, caption=f"Links for: {title}")
            bio.close()
            await status_msg.delete()
        else:
            await client.edit_message_text(
                chat_id=status_msg.chat.id,
                message_id=status_msg.id,
                text=output_message
            )
            await status_msg.delete()

    except Exception as e:
        logging.exception("Error while extracting links")
        try:
            await client.edit_message_text(
                chat_id=status_msg.chat.id,
                message_id=status_msg.id,
                text=f"❌ Error while extracting links: {e}"
            )
        except Exception:
            logging.exception("Failed to report error to user")

if __name__ == "__main__":
    app.run()