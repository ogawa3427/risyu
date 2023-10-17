import re
import os

with open('risyu20230924235801.csv', 'r', encoding='utf-8') as f:
	lines = f.readlines()

fifth_items = list(set([line.split(',')[5].strip() for line in lines if len(line.split(',')) >= 5]))

print(fifth_items)