import os

def get_files_info(working_directory, directory='.'):
    """Returns a string with information about files in the specified directory."""

    try:
        abs_working_directory=os.path.abspath(working_directory)
        abs_target_directory=os.path.abspath(os.path.join(working_directory, directory))

        if not abs_target_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(abs_target_directory):
            return f'Error: "{abs_target_directory}" is not a directory'
        

        def build_return_string(directory_contents):
            """Builds a return string with file information."""

            singel_item_propertys = []

            for item in directory_contents:
                item_size=os.path.getsize(os.path.join(abs_target_directory, item))
                item_is_dir=os.path.isdir(os.path.join(abs_target_directory, item))
                singel_item_propertys.append(f'- {item}: file_size={item_size} bytes, is_dir={item_is_dir}')

            return '\n'.join(singel_item_propertys)
        
            
        return build_return_string(os.listdir(abs_target_directory))
    
    # Catch any unexpected errors and return as string so LLM can handle it gracefully
    except Exception as e:
        return f'Error: {str(e)}'


