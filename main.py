import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import system_prompt
from functions.call_functions import available_functions, call_function

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("The api key is missing or not found")
    
    
    client = genai.Client(api_key=api_key)

    messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
        ]
    if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")
    
    for i in range(20):
        res = generate_content(client, messages, args.verbose)
        if res:
            break
        if i == 20:
            sys.exit("Something went wrong")


def generate_content(client: genai.Client, messages: list[types.Content], verbose: bool) -> None:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if response.candidates:
        for res in response.candidates:
            messages.append(res)

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return True

    function_result = []

    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if not function_call_result.parts:
            raise Exception("The list of parts its empty")
        if function_call_result.parts[0].function_response is None:
            raise Exception("The object from response is missing")
        if function_call_result.parts[0].function_response.response is None:
            raise Exception("The response from the function is missing")
        
        function_result.append(function_call_result.parts[0])
        

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    messages.append(types.Content(role="user", parts=function_result))
    

if __name__ == "__main__":
    main()
