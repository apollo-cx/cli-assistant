import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")
client=genai.Client(api_key=api_key)

def _parse_args(argv):
    
    user_prompt = ""
    flags = []

    for arg in argv:
        if arg.startswith("-") or arg.startswith("--"):
            flags.append(arg)
        else:
            user_prompt += arg + " "
    return user_prompt, flags


def main():

    user_prompt, flags = _parse_args(sys.argv[1:])

    if not user_prompt:
        print("Please provide input text as a command-line argument.")
        sys.exit(1)

    messages=[
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]    

    response=client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    prompt_tokens=response.usage_metadata.prompt_token_count
    response_tokens=response.usage_metadata.candidates_token_count

    if "--verbose" in flags or "-v" in flags:
        print(
            f"""
              \nUser prompt: {user_prompt}
              \nPrompt tokens: {prompt_tokens}
              \nResponse tokens: {response_tokens}\n
            """
        )
    
    print(response.text)
              
if __name__ == "__main__":
    main()
