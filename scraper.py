import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin


def fetch_webpage(url):
    if not url.startswith("http"):
        url = "https://" + url
    headers = {'User-Agent': 'Mozilla/5.0'}
    return requests.get(url, headers=headers).text


def make_soup(html):
    return BeautifulSoup(html, "html.parser")

def extract_data(soup, base_url):
    title = ""
    if soup.title:
        title = soup.title.string.strip()

    body = ""
    if soup.body:
        body = soup.body.get_text(" ", strip=True)

    links = []
    for tag in soup.find_all("a", href=True):
        full_url = urljoin(base_url, tag["href"])
        links.append(full_url)

    return title, body, links


url = sys.argv[1]

html = fetch_webpage(url)
soup = make_soup(html)

title, body, links = extract_data(soup, url)

print(title)
print(body)

for link in links:
    print(link)