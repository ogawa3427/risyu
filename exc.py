import json

with open('2024q1.tsv', 'r', encoding='utf-8') as file:
    lines = file.readlines()
lines = [line.strip() for line in lines]
lines = [line.split('\t') for line in lines]
print(lines)