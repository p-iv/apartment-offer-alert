import asyncio
from telegram import Bot
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


async def send_telegram_notification_async(offer_data, is_valuable = False):
    bot = Bot(token=TOKEN)

    header = "🔥 <b>NOWA OFERTA WYNAJMU (Okazja &lt;-15%)</b> 🔥" if is_valuable else "<b>NOWA OFERTA WYNAJMU</b>"

    message = (
        f"{header}\n\n"
        f"📌 <b>Tytuł:</b> {offer_data['title']}\n"
        f"💰 <b>Cena:</b> {int(offer_data['price'])} zł\n"
        f"📐 <b>Metraż:</b> {offer_data['apartment_size']} m²\n"
        f"💵 <b>Cena za m²:</b> {offer_data['price_per_m2']:.2f} zł/m²\n\n"
        f"🔗 <a href='{offer_data['url']}'>Check offer on otodom</a>"
    )

    try:
        if offer_data.get('image') and offer_data['image'].startswith('http'):
            await bot.send_photo(
                chat_id=CHAT_ID,
                photo=offer_data['image'],
                caption=message,
                parse_mode=ParseMode.HTML
            )
        else:

            await bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False
            )
        print(f"[Telegram] Message sent for: {offer_data['title']}")
        return True
    except Exception as e:
        print(f"[Telegram] Error: {e}")
        return False


def send_telegram_notification(offer_data, is_valuable = False):
    return asyncio.run(send_telegram_notification_async(offer_data, is_valuable))