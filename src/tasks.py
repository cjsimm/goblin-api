from pathlib import Path

from src.constants import FLEETING_NOTE_PATH, MARKDOWN_COLLECTION_PATH
from src.markdown import (
    FLEETING_NOTE_TEMPLATE,
    TEMPLATE_PATH,
    format_fleeting_note_filename,
    write_template_to_markdown_collection,
)


async def process_fleeting_note(raw_text: str) -> Path:
    """
    Processes the text of a validated note, injecting it into the Fleeting Note template and adding it to the markdown collection directory ready to be synced to the git origin. Returns a Path object pointing to the new fleeting note markdown file
    """
    target_path = FLEETING_NOTE_PATH / format_fleeting_note_filename(raw_text)
    write_template_to_markdown_collection(
        raw_text, TEMPLATE_PATH / FLEETING_NOTE_TEMPLATE, target_path
    )
    return target_path.relative_to(MARKDOWN_COLLECTION_PATH)
