from threading import Thread

from telebot import TeleBot
from telebot.types import Message

from src import msg_templates


def _start_message(message: Message, bot: TeleBot):
    bot.reply_to(message, msg_templates.CURRENT_CHAT_ID.format(chat_id=message.chat.id))


def build_bot(token: str) -> TeleBot:
    bot = TeleBot(token, parse_mode="MARKDOWN", num_threads=1)
    bot.register_message_handler(_start_message, pass_bot=True, commands=["start"])
    return bot



def create_bot_thread(bot: TeleBot) -> Thread:
    return Thread(
        target=bot.infinity_polling,
        kwargs={"timeout": 10, "long_polling_timeout": 10},
        daemon=True,
    )

