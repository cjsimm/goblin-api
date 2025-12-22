"""constants.py

constants and env variables/secrets required by the application and api
"""

import os
from pathlib import Path

def get_env_var(env_var_name: str, *, allow_empty=False) -> str:
    """Get env var or throw error"""
    var = os.getenv(env_var_name, "")
    if not var and not allow_empty:
        raise ValueError(f"env var {env_var_name} is not set")
    return var

ZK_BOT_TOKEN = get_env_var("ZK_BOT_TOKEN")
MARKDOWN_COLLECTION_DIR = get_env_var("MARKDOWN_COLLECTION_DIR")
FLEETING_NOTE_DIR = get_env_var("FLEETING_NOTE_DIR", allow_empty=True)


MARKDOWN_COLLECTION_PATH = Path(".", MARKDOWN_COLLECTION_DIR)
print(MARKDOWN_COLLECTION_PATH)

if not MARKDOWN_COLLECTION_PATH.exists():
    raise NotADirectoryError(f"'{MARKDOWN_COLLECTION_PATH}' is not a directory")

FLEETING_NOTE_PATH = MARKDOWN_COLLECTION_PATH / FLEETING_NOTE_DIR
FLEETING_NOTE_PATH.mkdir(exist_ok=True)
