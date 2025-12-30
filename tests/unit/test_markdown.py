from enum import Enum
from pathlib import Path

import pytest

from src.markdown import write_template_to_markdown_collection


class NoteTemplate(Enum):
    FLEETING_NOTE = "this is a test note \n{capture}"

    def __str__(self) -> str:
        return self.value


@pytest.mark.parametrize("template_file", list(NoteTemplate))
def test_write_template_to_markdown_collection(
    template_file: NoteTemplate, tmp_path: Path
) -> None:
    """Test that data is correctly injected into a template str opened from the filesystem"""
    expected_interpolation = "expected_interpolation even / with escape chars"
    template_path = tmp_path / "test_template.md"
    template_path.write_text(str(template_file))
    output = write_template_to_markdown_collection(
        expected_interpolation, template_path, tmp_path / "output_note.md"
    )
    assert output == str(template_file).format(capture=expected_interpolation)
