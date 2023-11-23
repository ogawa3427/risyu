import re

with open ('1306.htm', 'r', encoding='utf-8') as f:
    sample_html = f.read()

pattern = re.compile(
    r"<td>(.*?)</td><td align=\"left\">(.*?)</td><td>(.*?)</td><td>(.*?)</td><td align=\"left\">(.*?)</td><td>(.*?)</td><td>(.*?)</td><td align=\"center\">\s+<span.*?>(.*?)</span>"
)

# Using re.findall to extract all occurrences of the pattern
extracted_data = re.findall(pattern, sample_html)

print(extracted_data)