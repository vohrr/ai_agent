from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from google.genai import types

ALLOWED_FUNCTIONS = {
    'get_files_info' : get_files_info,
    'get_file_content' : get_file_content,
    'write_file' : write_file,
    'run_python_file' : run_python_file   

}

def call_function(function_call, working_directory, verbose=False):
    if not function_call.name in ALLOWED_FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    if verbose:
        print(f'Calling function:  {function_call.name}' + f'({function_call.args})') 
    else:
        print(f'- Calling function:  {function_call.name}') 

    args = function_call.args.copy()
    args['working_directory'] = working_directory
    function_result = ALLOWED_FUNCTIONS[function_call.name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call.name,
                response={"result": function_result},
            )
        ],
    )
