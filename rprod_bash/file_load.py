from concurrent.futures import ThreadPoolExecutor

from rprod.database import (
    set_buffer as database_set_buffer,
    need_buffer as database_need_buffer,
)
from rprod.calculate_checksum import calculate_checksum
from .message import message as msg


def calculate_file_checksum(filename: str) -> str:
    """Calculate a file checksum"""
    with open(filename, "rb") as f:
        buffer = f.read()
    checksum = calculate_checksum(buffer)
    return checksum


def register_file(filename: str) -> str:
    """Calculate a file checksum and put it in the database."""
    with open(filename, "rb") as f:
        buffer = f.read()
    checksum = calculate_checksum(buffer)
    database_set_buffer(checksum, buffer)
    return checksum


def check_file(filename: str) -> tuple[bool, int]:
    """Check if a file needs to be written to the database.
    Return the result, the checksum, and the length of the file buffer"""
    with open(filename, "rb") as f:
        buffer = f.read()
    checksum = calculate_checksum(buffer)
    result = database_need_buffer(checksum)
    return result, checksum, len(buffer)


def files_to_checksums(
    filelist: list[str],
    *,
    directories = list[str],
    max_files: int | None,
    max_datasize: int | None,
    nparallel: int = 20
):
    """Convert a list of filenames to a dict of filename-to-checksum items
    In addition, each file buffer is added to the database.

    max_files: the maximum number of files to send to the database.
    max_datasize: the maximum data size (in bytes) to send to the database.
    nparallel: number of files to process simultaneously
    directories: entries in filelist that are directories instead of files
    """

    db_put = True

    if len(directories):
        raise NotImplementedError

    """
    TODO: if the database has been started locally, set db_put to false
    we can then add the filenames directly.    
    This is done using a "filenames" request to the DB
    See the seamless-tools Git branch "database-filenames" 
    """

    result = {}
    if db_put:
        with ThreadPoolExecutor(max_workers=nparallel) as executor:
            filelist2 = []
            datasize = 0
            func = check_file
            for filename, curr_result in zip(filelist, executor.map(func, filelist)):
                needs_buffer, checksum, buffer_length = curr_result
                result[filename] = checksum
                if needs_buffer:
                    msg(
                        2,
                        "Not in database: '{}', checksum {}, length {}".format(
                            filename, checksum, buffer_length
                        ),
                    )
                    filelist2.append(filename)
                    datasize += buffer_length
                else:
                    msg(
                        2,
                        "Already in database: '{}', checksum {}, length {}".format(
                            filename, checksum, buffer_length
                        ),
                    )
        if not len(filelist2):
            return result
        if datasize > 10**9:
            size = "{:.2f} GiB".format(datasize / 10**9)
        elif datasize > 10**6:
            size = "{:.2f} MiB".format(datasize / 10**6)
        elif datasize > 10**4:
            size = "{:.2f} KiB".format(datasize / 10**3)
        else:
            size = "{} bytes".format(datasize)
        msg(0, "Upload {} files, total {}".format(len(filelist2), size))
        # TODO: confirmation from terminal, if available.
        if max_files is not None and len(filelist2) > max_files:
            raise ValueError(
                """Too many files to be uploaded without confirmation.
If you want to proceed, repeat the rprod command with '-y'."""
            )
        if max_datasize is not None and datasize > max_datasize:
            raise ValueError(
                """Too many files to be uploaded without confirmation.
If you want to proceed, repeat the rprod command with '-y'."""
            )
        filelist = filelist2
        func = register_file
    else:
        func = calculate_file_checksum
        result = {}

    with ThreadPoolExecutor(max_workers=nparallel) as executor:
        for filename, checksum in zip(filelist, executor.map(func, filelist)):
            result[filename] = checksum
    return result
