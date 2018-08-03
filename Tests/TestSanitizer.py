import unittest
from Engine import Sanitizer
import string
from functools import reduce

VALID_CHARS = string.ascii_letters + string.digits + "~_."


def validate_path(the_string):
    mapped = list(map(lambda char: char in VALID_CHARS, the_string))
    return False not in mapped


class Test_Sanitizer(unittest.TestCase):
    def test_the_donald_string(self):
        the_string = 'WATCH_PARTY_President_Trump_Rally_-_Wilkes-Barre_PA_-_8/2/18.json'
        sanitized = Sanitizer.sanitize_filename(the_string)
        self.assertTrue(validate_path(sanitized))


if __name__ == "__main__":
    unittest.main()

