import os 
from functions.config import MAX_FILE_LENGTH  

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:  
        with open(abs_file_path, "r") as fs:
            file_contents = fs.read()
            if len(file_contents) > MAX_FILE_LENGTH:
                file_contents = f"""{file_contents[:MAX_FILE_LENGTH]} 
                [...File "{file_path}" truncated at {MAX_FILE_LENGTH} characters]""" 

            return file_contents

    except Exception as e:
        return f'Error: unable to read file contents for "{file_path}", exception message: {e}'

