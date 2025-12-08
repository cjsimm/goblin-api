from fastapi import APIRouter, BackgroundTasks, Response
from pydantic import BaseModel

from src.constants import FLEETING_NOTE_PATH, MARKDOWN_COLLECTION_PATH
from src.markdown import (
    FLEETING_NOTE_TEMPLATE,
    TEMPLATE_PATH,
    sync_note_to_origin,
    write_template_to_markdown_collection,
)


class TelegramUpdate(BaseModel):
    """Schema representing an API Update, the main JSON format served from the
    Telegram Bot API informing an application of updates to bot channels
    """


zk = APIRouter(prefix="/zk")


@zk.post("/fleeting")
async def create(background_tasks: BackgroundTasks) -> Response:
    """Create a fleeting zk note and add it to an obsidian vault in the unsorted category"""
    original_note = "placeholder"
    target_path = FLEETING_NOTE_PATH / original_note
    write_template_to_markdown_collection(
        original_note, TEMPLATE_PATH / FLEETING_NOTE_TEMPLATE, target_path
    )
    new_file_relative_path = target_path.relative_to(MARKDOWN_COLLECTION_PATH)
    background_tasks.add_task(sync_note_to_origin, new_file_relative_path)
    return Response()
