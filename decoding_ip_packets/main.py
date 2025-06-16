import requests

def fetch():
    requests.get("https://kali.org")

for _ in range(10):
    fetch()

