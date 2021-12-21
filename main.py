import aiogram
from fastapi import FastAPI

from functools import partial

import logging
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, Update

TOKEN = "914543704:AAGxCfEN279RPLCAFsFTsQR2ava6P13c5ZE"
dp = Dispatcher()

logger = logging.getLogger(__name__)

bots = {
    TOKEN: Bot(TOKEN, parse_mode="HTML")
}

app = FastAPI()

@dp.message(commands={"start"})
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    # Most of event objects has an aliases for API methods to be called in event context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage` method automatically
    # or call API method directly via Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")


@dp.message()
async def echo_handler(message: types.Message) -> Any:
    """
    Handler will forward received message back to the sender
    By default message handler will handle all message types (like text, photo, sticker and etc.)
    """
    try:
        # Send copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


def main() -> None:
    # Initialize Bot instance with an default parse mode which will be passed to all API calls
    # And the run events dispatching
    for token, bot in bots.values():
        app.add_api_route(f"/bot/{token}", partial(process_bot_update, bot_token=token))



async def process_bot_update(update: Update, bot_token: str = ""):    
    dp.feed_webhook_update()

