"""utils.py

Module to hold utility functions and constants that have reuse value across the
entire project
"""


def set_telegram_webhook(bot_token: str, target_endpoint: str) -> None:
    """Setup a telegram webhook for a specific bot to post updates to within
    the api. This should be run when first setting up a fresh bot, or when a
    url needs to be reset
    """
