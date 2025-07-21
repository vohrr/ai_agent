import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model = 'gemini-2.0-flash-001'

def main(prompt):
    if len(prompt) == 0 or prompt == None:
        print("Please enter a valid prompt.")
        return
    response = client.models.generate_content(model=model, contents=prompt)
    print(response.text)

    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("One question at a time please!")
        exit(1)
    main(sys.argv[-1])
