import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_dir):
        return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        result = ""
        for directory in os.listdir(target_dir):
            sub_directory_path = os.path.join(target_dir, directory)
            file_size = get_dir_size(sub_directory_path)
            result += f"- {directory}: file_size={file_size} bytes, is_dir={os.path.isdir(sub_directory_path)}\n"
        return result
    except Exception as e:
        return f'Error listing files: {e}'

def get_dir_size(directory):
    if not os.path.isdir(directory):
        return os.path.getsize(directory) 
    directory_size = 0;
    for inner_directory in os.listdir(directory):
        inner_path = os.path.join(directory, inner_directory)
        directory_size += get_dir_size(inner_path)
    return directory_size


