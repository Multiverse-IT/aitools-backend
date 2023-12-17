import requests
from bs4 import BeautifulSoup

def check_link(url, target_link):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print("soup:", soup)
    all_links = [link.get('href') for link in soup.find_all('a')]

    if target_link in all_links:
        return True
    else:
        return False

website_url = 'https://www.supplers.com/'
target_url = '/public/news'
result = check_link(website_url, target_url)

if result:
    print(f"The link {target_url} is present on the website.")
else:
    print(f"The link {target_url} is not present on the website.")