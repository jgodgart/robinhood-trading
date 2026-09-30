from bs4 import BeautifulSoup

with open('/Users/jacobgodgart/.gemini/antigravity/brain/7fe28b16-2212-47df-9b98-dbd0dcbc560f/.system_generated/steps/85/content.md', 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')
print(soup.get_text(separator='\n', strip=True))
