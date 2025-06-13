import requests
from bs4 import BeautifulSoup

url = "https://gardening.usask.ca/articles-and-lists/articles-how-to/rotating-vegetables.php"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Step 2: Parse the HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Extract all text from the main content
# You can look for specific elements like <p>, <li>, <table>, etc.
all_paragraphs = soup.find_all(['p', 'li'])

# Step 4: Combine the text
text_data = ""
for tag in all_paragraphs:
    line = tag.get_text(strip=True)
    if line:
        text_data += line + "\n"

# Optional: Save to a text file
with open("crop_rotation_tnau.txt", "w", encoding="utf-8") as f:
    f.write(text_data)

print("Scraped and saved content successfully.")
