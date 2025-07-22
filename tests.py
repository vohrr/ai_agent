import unittest
from functions.get_files_info import get_files_info 

def main():
    print(f"Result for current directory:")
    print(get_files_info('calculator', '.'))

    print(f"Result for 'pkg' directory:")
    print(get_files_info('calculator', 'pkg'))

    print(f"Result for '/bin' directory:")
    print(get_files_info('calculator', '/bin'))

    print(f"Result for '../' directory:")
    print(get_files_info('calculator', '../'))
    
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
#    unittest.main()
    main()
