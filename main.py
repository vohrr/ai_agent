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
Looking in subdirectories of the working directory is acceptable in order to find the relevant files.
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
    # generate first response based on user prompt
    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    #use a loop to keep calling generate_content, cap it at 20 iterations
    for _ in range(20):
        #add the response candidates to our conversion (messages)
        if response.candidates is not None:
            for candidate in response.candidates:
                if candidate.content is not None:
                    for part in candidate.content.parts:
                        if part.text is not None:
                            print(f"Model: {part.text}")
                    messages.append(candidate.content) 

        if response.function_calls is not None:
            print(f"I want to call: {response.function_calls[0].name}")
            for function in response.function_calls:
                function_response_parts = call_function(function, working_directory, verbose).parts

                if function_response_parts is not None and len(function_response_parts) != 0:
                    function_response = function_response_parts[0].function_response

                    if function_response is None or function_response.response is None:
                        print(f"Something went wrong")
                        exit(1)

                    if verbose:
                        print(f" -> {function_response.response}")
                    #use the types.Content function to convert the function_response into a 
                    # message with the role of tool and append it into your message
                    new_message = types.Content(role="model", parts=function_response_parts)
                    messages.append(new_message)
                    response = client.models.generate_content(
                            model=model,
                            contents=messages,
                            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
                    )
        else:
            print(f"Final response: {response.text}")
            break;

    if verbose and response.usage_metadata is not None:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("One question at a time please!")
        exit(1)

    main(sys.argv[1], "--verbose" in sys.argv)
