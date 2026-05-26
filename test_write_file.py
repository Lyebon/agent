from functions.get_files_info import write_file
import unittest

class TestGet_files(unittest.TestCase):    
    def test_write_file(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        result1 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        result2 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        print(result1)
        print(result2)

if __name__ == "__main__":
    unittest.main()