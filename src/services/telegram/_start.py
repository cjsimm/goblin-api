from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.ext.filters import User

from src.constants import TG_USER_ID


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None:
        # somehow start has begun without a chat id
        return
    await ctx.bot.send_message(
        update.effective_chat.id,
        "Markdown ZK Bot Enabled! Messages sent in this chat will be created as fleeting notes in your slipbox!",
    )


start_handler = CommandHandler("start", start, filters=User(TG_USER_ID))
