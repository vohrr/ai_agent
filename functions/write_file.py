import os 

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: cannot write to "{file_path}" as it is outside the permitted working directory'

    subdirs = file_path.split('/')

    for i in range(0, len(subdirs)-1):
        abs_subdir = os.path.abspath(os.path.join(working_directory, subdirs[i]))
        if not os.path.exists(abs_subdir):
            return f'Error: unable to create "{file_path}" in "{working_directory}"'

    with open(abs_file_path, 'w') as file_stream:
        try:
            file_stream.write(content)
        except Exception as e:
            return f'Error: unable to write contents to "{file_path}": "{e}"'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)' 
