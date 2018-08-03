import os

RESERVED_CHARACTERS_ELIMINATE = ['<', '>', ':', '"', '/', '|', '?', '*']
RESERVED_CHARACTERS_UNDERSCORE = [' ', '\\']
MAX_FILE_PATH_LENGTH = 260


class SanitizationError(Exception):
    pass


def sanitize_filename(file_name):
    for character in RESERVED_CHARACTERS_ELIMINATE:
        file_name = file_name.replace(character, '')

    for character in RESERVED_CHARACTERS_UNDERSCORE:
        file_name = file_name.replace(character, '_')
    return file_name


def trim_file_path(file_path):
    if len(file_path) > MAX_FILE_PATH_LENGTH:
        split_file_path = os.path.split(file_path)
        
        if len(split_file_path[0]) > MAX_FILE_PATH_LENGTH:
            raise SanitizationError("Cannot shorten filepath sufficiently. Please move your root folder to the lowest"
                                    " directory you can.")
        
        name, ext = os.path.splitext(split_file_path[1])
        max_file_name_length = MAX_FILE_PATH_LENGTH - (len(split_file_path[0]) + len(ext) + 2)  # +1 for \ & . to rejoin
        name = name[0:max_file_name_length]
        full_name = '{}.{}'.format(name, ext)
        file_path = os.path.join(split_file_path[0], full_name)

    return file_path


