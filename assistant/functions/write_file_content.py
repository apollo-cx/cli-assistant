"""File writing function with directory auto-creation.

Writes or overwrites files within the working directory,
automatically creating parent directories as needed.
"""

import os


def write_file(working_directory, file_path, content):
    """Write content to a file within the working directory.

    Args:
        working_directory: Base directory that all operations are restricted to.
        file_path: Path to the file relative to working_directory.
        content: String content to write to the file.

    Returns:
        Success message with character count, or error message if:
        - File path is outside the working directory
        - Any exception occurs during writing

    Parent directories are created automatically if they don't exist.
    Existing files are overwritten without warning.
    """

    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_file.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_target_file):
            os.makedirs(os.path.dirname(abs_target_file), exist_ok=True)

        with open(abs_target_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
