"""
Callback handler dealing with fleeting note submissions to the telegram bot
"""

from telegram.ext import ContextTypes, MessageHandler

from src.markdown import sync_note_to_origin
from src.tasks import process_fleeting_note
from telegram import Update


async def fleeting_note(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Callback handler that processes fleeting notes sent via the webhook. acts as an adapter to unpack the relevant data from the Telegram Update object"""
    # update.message might be null. how are you meant to deal with this
    # according to the framework? - cant find the answer, seems like there's no
    # way to automatically narrow. will just run a check for now and try to
    # deal with it later with a customercontext instead
    if update.message is None:
        # logging message here that the update came through without a message.
        # We should never hit this because the callback is tied to a
        # messagehandler that ensures a message is present before running the
        # callback
        print("logging message here")
        return
    if update.message.text is None:
        print("logging that there was no text in the message")
        return
    file_path = await process_fleeting_note(update.message.text)
    sync_note_to_origin(file_path)
    await update.message.reply_text("received a message via the webhook")


fleeting_note_handler = MessageHandler(None, fleeting_note)
