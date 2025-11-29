from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file
from functions.run_python import run_python


def test_get_files_info():
    print(f"Result for current directory:\n{get_files_info("calculator", ".")}\n\n")
    print(f"Result for 'pkg' directory:\n{get_files_info("calculator", "pkg")}\n\n")
    print(f"Result for '/bin' directory:\n{get_files_info("calculator", "/bin")}\n\n")
    print(f"Result for '../' directory:\n{get_files_info("calculator", "../")}\n\n")


def test_get_file_content():
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


def test_write_to_file():
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


def test_run_python():
    print(run_python("calculator", "main.py"))
    print(run_python("calculator", "main.py", ["3 + 5"]))
    print(run_python("calculator", "tests.py"))
    print(run_python("calculator", "../main.py"))
    print(run_python("calculator", "nonexistent.py"))
    print(run_python("calculator", "lorem.txt"))


test_run_python()
