from subprocess import run
import unittest
from functions.get_files_info import get_files_info 
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

def get_files_info_tests():
    print(f"Result for current directory:")
    print(get_files_info('calculator', '.'))

    print(f"Result for 'pkg' directory:")
    print(get_files_info('calculator', 'pkg'))

    print(f"Result for '/bin' directory:")
    print(get_files_info('calculator', '/bin'))

    print(f"Result for '../' directory:")
    print(get_files_info('calculator', '../'))
    
def get_file_content_tests():
    print(get_file_content("calculator", "lorem.txt"))
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


def write_file_tests():
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

def run_python_tests():
    print(run_python_file("calculator", "main.py"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print(run_python_file("calculator", "tests.py"))
    print(run_python_file("calculator", "../main.py"))
    print(run_python_file("calculator", "nonexistent.py"))

class AiAgentTests(unittest.TestCase):
    
    def test_get_calculator_current_directory(self):
        result = get_files_info("calculator", ".")
        self.assertEqual("calculator/", result)

    def test_get_calculator_outer_directory(self):
        result = get_files_info("calculator", "../")
        self.assertEqual('Error. Cannot list "../" as it is outside the permitted working directory', result)
    
    def test_get_calculator_inner_directory(self):
        result = get_files_info("calculator", "pkg")
        self.assertEqual("calculator/pkg", result)

if __name__ == "__main__":
    # unittest.main()
    # get_files_info_tests()
    # get_file_content_tests()
    # write_file_tests()
    run_python_tests()
