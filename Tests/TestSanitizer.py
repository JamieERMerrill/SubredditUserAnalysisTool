import unittest
from Engine import Sanitizer
import os

HERE = os.path.abspath(os.path.dirname(__file__))

def try_write(full):
    if os.path.exists(full):
        return
    try:
        fp = open(full, 'w')
        fp.close()
    finally:
        try:
            os.remove(full)
        except Exception as e:
            print("FAILED TO CLEANUP. FILE MAY NOT EXIST.")
            raise e


class Test_Sanitizer(unittest.TestCase):
    def test_the_donald_string(self):
        the_string = 'WATCH_PARTY_President_Trump_Rally_-_Wilkes-Barre_PA_-_8/2/18.json'
        sanitized = Sanitizer.sanitize_filename(the_string)
        full = os.path.join(HERE, sanitized)
        try_write(full)

    def test_too_long_name(self):
        the_file_name = 'CORGI' * 500
        full = os.path.join(HERE, the_file_name)
        try:
            sanitized_full = Sanitizer.trim_file_path(full)
        except Sanitizer.SanitizationError:
            print("BASE FILEPATH WAS TOO LONG - TEST IS ABORTING")
            raise

        try_write(sanitized_full)


if __name__ == "__main__":
    unittest.main()

