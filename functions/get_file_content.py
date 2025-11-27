import os
from functions.config import MAX_CHARS


def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_file.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read and possibly truncate
        if os.path.getsize(abs_target_file) > MAX_CHARS:
            with open(abs_target_file, "r") as f:
                file_content = f.read(MAX_CHARS)
            file_content += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        else:
            with open(abs_target_file, "r") as f:
                file_content = f.read()

        return file_content

    except Exception as e:
        return f"Error: {str(e)}"
