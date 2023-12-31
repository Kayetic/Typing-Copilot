from pynput import keyboard
import requests
import pyperclip
import keyboard as kb
import os
import argparse


parser = argparse.ArgumentParser(description='A text completer tool similar to Github Copilot for for any text.')
parser.add_argument('--tokens', type=int, default=32, help='The maximum number of tokens to generate.')
args = parser.parse_args()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def fetch_completion(prompt, max_tokens):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    data = {
        "model": "gpt-3.5-turbo-instruct",
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0
        # Note: 'stream': True is removed as we are using synchronous requests
    }
    response = requests.post(url, headers=headers, json=data)
    completion_data = response.json()
    print(completion_data)

    if 'choices' in completion_data and len(completion_data['choices']) > 0:
        text_chunk = completion_data['choices'][0]['text']
        print(text_chunk)
        kb.write(text_chunk, 0.025)

def on_activate():
    prompt_text = getPastText()
    fetch_completion(prompt_text, args.tokens)

def main():
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+f': on_activate}) as h:
        h.join()

def getPastText():
    # Press command and shift and the up arrow 5 times to select the previous 5 lines
    # Press command c to copy
    # Get the clipboard contents to use
    kb.press_and_release('command+shift+up')
    # copy the selected text
    keys = keyboard.Controller()
    keys.press('<ctrl>+c')

    # Get the clipboard contents
    past_text = pyperclip.paste()
    return past_text

if __name__ == "__main__":
    main()
    
