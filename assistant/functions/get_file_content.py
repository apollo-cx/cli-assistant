"""File content reading function with security and size constraints.

Reads file contents from within the working directory, with automatic
truncation for large files to prevent memory issues.
"""

import os

from assistant.config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """Read the contents of a file within the working directory.

    Args:
        working_directory: Base directory that all operations are restricted to.
        file_path: Path to the file relative to working_directory.

    Returns:
        The file contents as a string, or an error message if:
        - File is outside the working directory
        - File doesn't exist or is not a regular file
        - Any other exception occurs

    Files larger than MAX_CHARS are truncated with a notice appended.
    """
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
