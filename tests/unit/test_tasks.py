import pytest

from src.tasks import process_fleeting_note


@pytest.mark.asyncio
@pytest.mark.parametrize("raw_text", ["test text with a / in the data"])
async def test_process_fleeting_note(raw_text: str) -> None:
    await process_fleeting_note(raw_text)
