import requests
from bs4 import BeautifulSoup


def check_code_presence(url, target_code):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    page_content = str(soup)  # Convert the soup object to a string

    if target_code in page_content:
        return True
    else:
        return False

# website_url = 'https://www.supplers.com/'
# target_url = '/public/news'
# result = check_link(website_url, target_url)

# if result:
#     print(f"The link {target_url} is present on the website.")
# else:
#     print(f"The link {target_url} is not present on the website.")