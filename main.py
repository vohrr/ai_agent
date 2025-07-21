import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = 'gemini-2.0-flash-001'

def main(user_prompt, verbose):

    if verbose: 
        print(f"User prompt: {user_prompt}")

    if len(user_prompt) == 0 or user_prompt == None:
        print("Please enter a valid prompt.")
        return
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(model=model, contents=messages)
    print(response.text)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("One question at a time please!")
        exit(1)

    main(sys.argv[1], "--verbose" in sys.argv)
