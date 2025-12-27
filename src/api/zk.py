from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, Response
from pydantic import BaseModel

from src.constants import FLEETING_NOTE_PATH, MARKDOWN_COLLECTION_PATH
from src.markdown import (
    FLEETING_NOTE_TEMPLATE,
    TEMPLATE_PATH,
    sync_note_to_origin,
    write_template_to_markdown_collection,
)
from src.services.telegram import queue_webhook_payload


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


# This endpoint needs to be protected with a signed key telegram offers a
# header with a token that's set upon webhook setup
# X-Telegram-Bot-Api-Secret-Token. on application startup, need to generate
# this token, sign it with a key, and descrypt on every request through. On
# localhost development, this url needs to also be exposed via ngrok or some
# other local host tunneling app. Going to use the update polling for now to
# push forward with development
@zk.post("/telegram")
async def bot(
    payload: dict = Body(
        ..., description="Update object defined in the Telegram Bot API", example=""
    ),
) -> Response:
    """Webhook listeners for telegram fleeting note bot"""
    try:
        await queue_webhook_payload(payload)
    except Exception:
        # log here
        raise HTTPException(400, "Could not parse update payload from Telegram")
    return Response(status_code=201)
