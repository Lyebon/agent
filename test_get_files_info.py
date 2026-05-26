from functions.get_files_info import get_files_info, get_file_content
import unittest

class TestGet_files(unittest.TestCase):
    def test_get_files_info(self):
        print(get_files_info("calculator", "."))
        print(get_files_info("calculator", "/bin"))
        print(get_files_info("calculator", "../"))
        print(get_files_info("calculator", "main.py"))

    def test_get_files_path(self):
        result = get_files_info("calculator", ".")
        print(f'Result for current directory:{result}')
        result2 = get_files_info("calculator", "pkg")
        print(f'Result for "pkg" directory:{result2}')
        result3 = get_files_info("calculator", "/bin")
        print(f'''Result for '/bin' directory:
{result3}''')
        result4 = get_files_info("calculator", "../")
        print(f'''Result for '../' directory:
{result4}''')



if __name__ == "__main__":
    unittest.main()