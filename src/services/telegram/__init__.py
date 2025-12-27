"""Functionality related to the Telegram messaging app"""

from telegram.ext import Application, Updater

from src.constants import API_PUBLIC_URL, ZK_BOT_TOKEN, ZK_WEBHOOK_KEY
from telegram import Update

from ._fleeting_note import fleeting_note_handler

# Define globally for easy access. Calls using this bot won't work unless
# start_application has been called
app = Application.builder().token(ZK_BOT_TOKEN).updater(None).build()


async def start_application() -> Application:
    """Build and start application. Determine update strategy and build
    appropriate app using .builder() functionality. When integrated with
    another asyncio event loop, the convenience methods start_polling and
    start_webhook can't be called without blocking the thread. The components
    of the bot must be started manually and then shutdown on exit with
    stop_application when the async loop attempts to exit"""
    if ZK_WEBHOOK_KEY is not None:
        raise NotImplementedError
        # get or set webhook
    updater = Updater(app.bot, update_queue=app.update_queue)
    await updater.initialize()
    await updater.start_polling(poll_interval=1)
    app.add_handler(fleeting_note_handler)
    await app.initialize()
    await app.start()
    return app


async def stop_application() -> None:
    """Stop the application manually"""
    if app.updater is not None:
        await app.updater.stop()
    await app.stop()
    await app.shutdown()


async def queue_webhook_payload(payload: dict) -> None:
    await app.update_queue.put(Update.de_json(data=payload, bot=app.bot))


async def get_webhook_info() -> None:
    """check if a webhook is already active for the bot or not"""


async def set_webhook() -> None:
    """set a webhook for the bot pointing to the api webhook endpoint"""
    # need to get and set the secret token, possibly even gen it if webhook urls disappear with each startup
    await app.bot.set_webhook(API_PUBLIC_URL, secret_token=None)
