import requests
from bs4 import BeautifulSoup

def collectNews():
    URL = "https://www.timesnownews.com/latest-news"

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all("a", class_="undefined", href=True)

    for result in results:
        descriptionHref = result["href"]
        title = result["title"]
        descriptionUrl = f"{URL}{descriptionHref}"
        print(title)
        print(descriptionUrl)