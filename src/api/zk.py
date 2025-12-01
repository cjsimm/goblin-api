from fastapi import APIRouter, BackgroundTasks, Response
from pydantic import BaseModel

from src.obsidian import FLEETING_NOTE_TEMPLATE, sync_note_to_origin, write_template_to_obsidian_vault

class TelegramUpdate(BaseModel):
    """Schema representing an API Update, the main JSON format served from the
    Telegram Bot API informing an application of updates to bot channels"""
    ...


zk = APIRouter(prefix="/zk")


@zk.post("/fleeting")
async def create(background_tasks: BackgroundTasks) -> Response:
    """
    Create a fleeting zk note and add it to an obsidian vault in the unsorted category
    """
    original_note = "placeholder"
    note_filename = write_template_to_obsidian_vault(original_note, FLEETING_NOTE_TEMPLATE)
    background_tasks.add_task(sync_note_to_origin, note_filename)
    return Response()
