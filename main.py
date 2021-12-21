from fastapi import FastAPI

import logging
from typing import Any, Dict
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, Update
from fastapi.params import Depends

webhook_url = "/bot/"

tokens = [""]

dp = Dispatcher()

logger = logging.getLogger(__name__)

bots: Dict[str, Bot] = {token: Bot(token, parse_mode="HTML") for token in tokens}
app = FastAPI()

async def bot_injector(token: str,):
    return bots[token]

@dp.message(commands={"start"})
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")


@dp.message()
async def echo_handler(message: types.Message) -> Any:
    """
    Handler will forward received message back to the sender
    By default message handler will handle all message types (like text, photo, sticker and etc.)
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def process_bot_update(update: Update, bot: Bot = Depends(bot_injector),):
    await dp.feed_webhook_update(bot, update)


@app.on_event("startup")
async def set_webhook():
    if (getenv('DETA_RUNTIME')):
        domain_prefix = getenv('DETA_PATH')
        for bot in bots.values():
            await bot.set_webhook(f"https://{domain_prefix}.deta.dev/{webhook_url}/{bot.token}")

# Initialize Bot instance with an default parse mode which will be passed to all API calls
# And the run events dispatching
app.add_api_route(f"{webhook_url}{{token}}", process_bot_update, methods=["POST"])
