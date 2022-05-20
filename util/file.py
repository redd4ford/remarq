from os.path import exists
from docx import Document

from util.exceptions import (
    FileNotReadable,
    FilepathNotProvidedError,
)


def is_path(path: str) -> str:
    """
    Check if a file with provided path exists.
    """
    if exists(path):
        return path
    raise FileNotFoundError(f'File does not exist: {path}')


def get_file_contents(filepath: str) -> list:
    """
    Parse the file by specified filepath and return text split into paragraphs.
    """
    if not filepath:
        raise FilepathNotProvidedError

    paragraphs = []
    # TODO(redd4ford): parsing from tables
    if filepath.endswith('.docx'):
        doc = Document(f'{filepath}')
        for paragraph in doc.paragraphs:
            paragraphs.append(paragraph.text)
    # TODO(redd4ford): support for more file extensions
    else:
        try:
            with open(f'{filepath}') as f:
                paragraphs = []
                for readline in f:
                    line_strip = readline.strip()
                    paragraphs.append(line_strip)
        except UnicodeDecodeError as err:
            raise FileNotReadable(filepath) from err
    return paragraphs
