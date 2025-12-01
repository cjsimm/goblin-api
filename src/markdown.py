"""
Implements operations and tasks related to collections of markdown files. These operations are useful to manipulate notes inside an obsidian vault
"""
from pathlib import Path
from src.git import GitClient

TEMPLATE_PATH = Path("src/templates")
# make this a symlink inside the folder?
MARKDOWN_COLLECTION_PATH = Path("obsidian-vault")

FLEETING_NOTE_TEMPLATE = "fleeting_note.md"

def write_template_to_markdown_collection(data: str, template_file: str) -> Path:
    """Inject data into a template file and save it to a directory inside the symlinked obsidian vault"""
    with open(TEMPLATE_PATH / template_file, 'r') as f:
        fleeting_template = f.read()
    # needs to be generalized. probably need a mapping between pydantic models and templates, then a parser for the note that can parse the string and organize the data for easy injection into the template
    note = fleeting_template.format(capture=data)
    new_filename = MARKDOWN_COLLECTION_PATH / data
    with open(new_filename, 'w') as f:
        f.write(note)
    return new_filename

def sync_note_to_origin(new_file: Path) -> None:
    """Add, commit, and push to origin a markdown file that has been created in the obsidian vault"""
    git = GitClient(MARKDOWN_COLLECTION_PATH)
    git.pull()
    git.add(new_file)
    # improve the commit message later. might need a dataclass/struct to start holding all the data
    git.commit("added new note")
    git.push()
