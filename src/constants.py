"""constants.py

constants and env variables/secrets required by the application and api
"""

import os
from pathlib import Path

ZK_BOT_TOKEN = os.getenv("ZK_BOT_TOKEN")
MARKDOWN_COLLECTION_DIR = os.getenv("MARKDOWN_COLLECTION_DIR")
FLEETING_NOTE_DIR = os.getenv("FLEETING_NOTE_DIR", "")

if MARKDOWN_COLLECTION_DIR is None:
    raise ValueError("MARKDOWN_COLLECTION_PATH is not populated with a value")

MARKDOWN_COLLECTION_PATH = Path(".", MARKDOWN_COLLECTION_DIR)
print(MARKDOWN_COLLECTION_PATH)

if not MARKDOWN_COLLECTION_PATH.exists():
    raise NotADirectoryError(f"'{MARKDOWN_COLLECTION_PATH}' is not a directory")

FLEETING_NOTE_PATH = MARKDOWN_COLLECTION_PATH / FLEETING_NOTE_DIR
FLEETING_NOTE_PATH.mkdir(exist_ok=True)
