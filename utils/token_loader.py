# token_loader.py
import json

def load_token(token_path):
    with open(token_path, 'r') as token_file:
        token_data = json.load(token_file)
    return token_data
