import unittest
from datetime import datetime
import mock

from ..reader import FileReader, ListReader


class ReaderTest(unittest.TestCase):
    @staticmethod
    def get_update(data):
        try:
            return next(data)
        except StopIteration:
            pass


class FileReaderTest(unittest.TestCase):
    def test_FileReader_opens_the_given_file(self):
        mock_open = mock.mock_open(read_data="")
        with mock.patch("__builtin__.open", mock_open, create=True):
            reader = FileReader("stocks.txt")
            updater = reader.get_updates()
            self.get_update(updater)
        mock_open.assert_called_with("stocks.txt", "r")

    @staticmethod
    def get_update(data):
        try:
            return next(data)
        except StopIteration:
            pass

    @mock.patch("__builtin__.open",
                mock.mock_open(read_data="""\
GOOG,2014-02-11T14:10:22.13,10"""))
    def test_FileReader_returns_the_file_contents(self):
        reader = FileReader("stocks.txt")
        updater = reader.get_updates()
        update = self.get_update(updater)
        self.assertEqual(("GOOG",
                          datetime(2014, 2, 11, 14, 10, 22, 130000),
                          10), update)

    @mock.patch("__builtin__.open",
                mock.mock_open(read_data="""\
GOOG,2014-02-11T14:10:22.13,10
MSFT,2014-02-11T00:00:00.0,8"""))
    def test_get_updates_returns_next_line_for_each_call(self):
        reader = FileReader("stocks.txt")
        updater = reader.get_updates()
        self.get_update(updater)
        update = self.get_update(updater)
        self.assertEqual(("MSFT", datetime(2014, 2, 11), 8), update)


class ListReaderTest(ReaderTest):
    def test_list_reader_returns_list_data_every_update(self):
        data = [("GOOG", datetime(2014, 2, 11), 3),
                ("AAPL", datetime(2014, 2, 11), 13)]
        reader = ListReader(data)
        updater = reader.get_updates()
        update = self.get_update(updater)
        self.assertEqual(("GOOG", datetime(2014, 2, 11), 3), update)
        update = self.get_update(updater)
        self.assertEqual(("AAPL", datetime(2014, 2, 11), 13), update)
