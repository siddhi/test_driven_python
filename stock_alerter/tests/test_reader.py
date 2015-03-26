import unittest
from unittest import mock
from datetime import datetime

from ..reader import FileReader


class FileReaderTest(unittest.TestCase):
    @mock.patch("builtins.open",
                mock.mock_open(read_data="""\
GOOG,2014-02-11T14:10:22.13,10"""))
    def test_FileReader_returns_the_file_contents(self):
        reader = FileReader("stocks.txt")
        updater = reader.get_updates()
        update = next(updater)
        self.assertEqual(("GOOG",
                          datetime(2014, 2, 11, 14, 10, 22, 130000),
                          10), update)
