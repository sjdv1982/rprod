from typing import Dict, List, Any

from .message import message as msg


def get_file_mapping(
    argdict: Dict[str, Any], mapping_mode: str
) -> Dict[str, str]:
    """Map files inside the transformation to files on disk.

    Arguments:

    - argdict:
    A dict of argument names and their types ("file", "directory", ...)
      obtained using `guess_arguments` or using an rprodfile.

    - mapping_mode:
    Must be one of:
    "literal": No mapping. All files must be inside the current working dir.
    "literal_strip": Strip directory names. After stripping, all files must be unique.
    "rename": Rename to file1, file2, ...
    "rename_with_ext": Same, but add the file extensions.

    Return: a dict where the key is the filename/dirname (pin name)
    inside the transformation and the value is the filename to be read
    from disk"""

    raise NotImplementedError  # stub
