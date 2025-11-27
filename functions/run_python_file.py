import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        if not abs_target_file.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_target_file):
            return f'Error: File "{file_path}" not found.'

        if not abs_target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            ["python", file_path] + args,
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=working_directory,
        )

        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced."

        result = (
            f"STDOUT: {completed_process.stdout}\n"
            f"STDERR: {completed_process.stderr}\n"
            f"{
                f'Process exited with code {completed_process.returncode}'
                if completed_process.returncode != 0 else ''
            }"
        )

        return result

    except Exception as e:
        return f"Error: executing Python file: {e}"
