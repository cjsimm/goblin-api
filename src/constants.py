"""constants.py

constants and env variables/secrets required by the application and api
"""

import os
from pathlib import Path


def get_env_var_allow_null(env_var_name: str, *, allow_empty=False) -> str | None:
    """Get env var or throw error"""
    var = os.getenv(env_var_name, None)
    if not var and not allow_empty:
        raise ValueError(f"env var {env_var_name} is not set")
    return var


def get_env_var(env_var_name: str) -> str:
    var = os.getenv(env_var_name, None)
    if var is None:
        raise ValueError(f"env var {env_var_name} is not set")
    return var


# ZK Telegram bot
ZK_WEBHOOK_KEY = get_env_var_allow_null("ZK_WEBHOOK_KEY", allow_empty=True)
ZK_BOT_TOKEN = get_env_var("ZK_BOT_TOKEN")
TG_USER_ID = int(get_env_var("TG_USER_ID"))

MARKDOWN_COLLECTION_DIR = get_env_var_allow_null("MARKDOWN_COLLECTION_DIR")
FLEETING_NOTE_DIR = get_env_var_allow_null("FLEETING_NOTE_DIR", allow_empty=True)

API_PUBLIC_URL = "https://www.cjsimm-webhook-test-yddda-dshs.com"

MARKDOWN_COLLECTION_PATH = (
    Path(".", MARKDOWN_COLLECTION_DIR)
    if MARKDOWN_COLLECTION_DIR is not None
    else Path()
)
print(MARKDOWN_COLLECTION_PATH)

if not MARKDOWN_COLLECTION_PATH.exists():
    raise NotADirectoryError(f"'{MARKDOWN_COLLECTION_PATH}' is not a directory")

FLEETING_NOTE_PATH = (
    MARKDOWN_COLLECTION_PATH / FLEETING_NOTE_DIR
    if FLEETING_NOTE_DIR is not None
    else MARKDOWN_COLLECTION_PATH
)
FLEETING_NOTE_PATH.mkdir(exist_ok=True)
