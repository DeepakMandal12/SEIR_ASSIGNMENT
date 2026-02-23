import requests
from bs4 import BeautifulSoup
import sys
import re
from collections import Counter

P = 53
MASK = (1 << 64) - 1



def fetch(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    return requests.get(url, headers=headers).text



def get_body(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.body.get_text(" ", strip=True) if soup.body else ""


def hash_word(word):
    h = 0
    power = 1
    for ch in word:
        h = (h + ord(ch) * power) & MASK
        power = (power * P) & MASK
    return h


def simhash(text):
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    freq = Counter(words)

    vector = [0] * 64

    for word, count in freq.items():
        h = hash_word(word)

        for i in range(64):
            if (h >> i) & 1:
                vector[i] += count
            else:
                vector[i] -= count

    fingerprint = 0
    for i in range(64):
        if vector[i] >= 0:
            fingerprint |= (1 << i)

    return fingerprint


# -------- Similarity --------
def common_bits(h1, h2):
    diff = bin(h1 ^ h2).count("1")
    return 64 - diff



if len(sys.argv) != 3:
    print("Usage: python script.py <url1> <url2>")
    sys.exit(1)

url1 = sys.argv[1]
url2 = sys.argv[2]

html1 = fetch(url1)
html2 = fetch(url2)

body1 = get_body(html1)
body2 = get_body(html2)

hash1 = simhash(body1)
hash2 = simhash(body2)

print(common_bits(hash1, hash2))