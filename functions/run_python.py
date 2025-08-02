import os 
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="""Runs the python file at the provided file_path.
                Accepts optional arguments to be passed into as arguments for the python file.
                Must be a python file.
                Constrained to the working directory.""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The location of the file to retrieve content from. Must be a file."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to be passed in to the python file.",
                items=types.Schema(type=types.Type.STRING),
                default=[]
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    #how do we put args into this 
    completed_process = subprocess.run(['uv', 'run', abs_file_path] + args,
                                   cwd=working_directory,
                                   capture_output=True,
                                   timeout=30)

    if completed_process.returncode != 0:
        return str(completed_process.stderr) + f' Process exited with code {completed_process.returncode}'
    else:
        return 'STDOUT: ' + str(completed_process.stdout)


if __name__ == "__main__":
    print(run_python_file('calculator', 'main.py'))
