# Python telegram bot on Deta with aiogram

- fastapi https://fastapi.tiangolo.com/ as webserver
- aiogram 3 https://docs.aiogram.dev/ as telegram bot framework
- deta https://docs.deta.sh/ as hosting system

[![Deploy](https://button.deta.dev/1/svg)](https://go.deta.dev/deploy?repo=https://github.com/Forevka/deta-python-bot)

## Prerequisites
Create new directory
```bash
mkdir python-telegram-bot && cd python-telegram-bot
```

Initialize deta project with
```bash
deta new
```

Specify requirements.txt file
```bash
fastapi
git+git://github.com/aiogram/aiogram.git@7c14a6b16b8f90dc4240802003cd89172adf7732#egg=aiogram
```
this will install fastapi and aiogram-v3

## Code

Imports explanation are omitted, i suppose that you know python basics.

```python
webhook_url = "/bot/"

tokens = ["914543704:AAGxCfEN279RPLCAFsFTsQR2ava6P13c5ZE"]

dp = Dispatcher()

logger = logging.getLogger(__name__)

bots: Dict[str, Bot] = {token: Bot(token, parse_mode="HTML") for token in tokens}
app = FastAPI()
```

Defines bot tokens, initialising bot objects and dispatcher for aiogram also creating fastapi application object.

```python
async def bot_injector(token: str,):
    return bots[token]

    
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
```
bot_injector - dependency injector for bot object.
process_bot_update - invoke aiogram update dispatch process.
set_webhook - set webhooks for all bot tokens that we defined before

## Deploying

just run command inside python-telegram-bot directory
```bash
deta deploy
```