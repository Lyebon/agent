import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.call_functions import available_functions, call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("The api key is missing or not found")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Gemini")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()


messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)


metadata = response.usage_metadata
if metadata is None:
    raise RuntimeError("The API request fail to fetch the response")
if args.verbose:
    print(
        f"User prompt: {args.user_prompt}\nPrompt tokens: {metadata.prompt_token_count}\nResponse tokens: {metadata.candidates_token_count}"
    )
else:
    print(response.text)

def main():
    print("Hello from agent!")


if __name__ == "__main__":
    main()
