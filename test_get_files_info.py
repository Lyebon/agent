from functions.get_files_info import get_files_info
import unittest

class TestGet_files(unittest.TestCase):
    def test_get_files_info(self):
        print(get_files_info("calculator", "."))
        print(get_files_info("calculator", "/bin"))
        print(get_files_info("calculator", "../"))
        print(get_files_info("calculator", "main.py"))

    def test_get_files_path(self):
        problem = get_files_info("calculator", ".")
        result = '''- main.py: file_size=719 bytes, is_dir=False
- tests.py: file_size=1331 bytes, is_dir=False
- pkg: file_size=44 bytes, is_dir=True
'''
        self.assertEqual(problem, result)

if __name__ == "__main__":
    unittest.main()