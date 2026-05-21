from functions.get_files_info import get_files_info
import unittest

class TestGet_files(unittest.TestCase):
    def test_get_files_info(self):
        print(get_files_info("calculator", "."))
        print(get_files_info("calculator", "/bin"))
        print(get_files_info("calculator", "../"))
        print(get_files_info("calculator", "main.py"))


if __name__ == "__main__":
    unittest.main()