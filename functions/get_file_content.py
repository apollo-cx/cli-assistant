import os
from re import M
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory=os.path.abspath(working_directory)
        abs_target_file=os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_file.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        def read_file_content(file):
            """Reads and returns the content of the file up to MAX_CHARS."""
            with open(abs_target_file, 'r') as file:
                file_content=file.read(MAX_CHARS)

            return file_content
        
        return read_file_content(abs_target_file)
    
    except Exception as e:
        return f'Error: {str(e)}'

print(get_file_content("calculator", "lorem.txt"))