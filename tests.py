from functions.get_files_info import get_files_info

def test_get_files_info():
    print(f"Result for current directory:\n{get_files_info("calculator", ".")}\n\n")
    print(f"Result for 'pkg' directory:\n{get_files_info("calculator", "pkg")}\n\n")
    print(f"Result for '/bin' directory:\n{get_files_info("calculator", "/bin")}\n\n")
    print(f"Result for '../' directory:\n{get_files_info("calculator", "../")}\n\n")

test_get_files_info()