import json
import os

with open('2023q3.json', 'r', encoding='utf-8') as f:
    rolelist = json.load(f)

print(rolelist.keys())