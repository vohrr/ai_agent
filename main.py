import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
working_directory = os.environ.get("WORKING_DIRECTORY")
client = genai.Client(api_key=api_key)
model = 'gemini-2.0-flash-001'
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
        schema_get_file_content,
    ])

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide must be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
Append the file extension to any requested file content in function parameters if not explicity provided 
"""

def main(user_prompt, verbose):

    if verbose: 
        print(f"User prompt: {user_prompt}")

    if len(user_prompt) == 0 or user_prompt == None:
        print("Please enter a valid prompt.")
        return
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if response.function_calls is not None:
        for function in response.function_calls:
            function_response = call_function(function, working_directory, verbose)
            if function_response.parts[0].function_response.response is None:
                print(f"Something went wrong")
                exit(1)
            if verbose:
                print(f" -> {function_response.parts[0].function_response.response}")
    else:
        print(response.text)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("One question at a time please!")
        exit(1)

    main(sys.argv[1], "--verbose" in sys.argv)
