import time
from db_util.writeNews import writeTitles
from bs4 import BeautifulSoup
from lib.constants import classic_news_type, english_language
import re
import requests


def getDescriptionUrl(URL, href):
    descriptionUrl = ""
    if "://" not in href:
        baseURL = create_base_url(URL)
        descriptionUrl = f"{baseURL}{href}"
    else:
        descriptionUrl = href
    return descriptionUrl


def create_base_url(full_url):
    # Check if the URL already has a scheme, if not, add "http://"
    if "://" not in full_url:
        full_url = "http://" + full_url

    # Find the index of the first slash after the scheme part
    first_slash_idx = full_url.find("/", full_url.index("://") + 3)

    # Extract the base URL
    base_url = full_url[:first_slash_idx]

    return base_url


def get_full_row(links, URL):
    data = []

    for link in links:
        href = link["href"]

        descriptionUrl = getDescriptionUrl(URL, href)

        data.append({"type": classic_news_type, "title": link["text"], "descriptionUrl": descriptionUrl,
                     "content": None, "language": english_language, "source": URL})

    return data


# basically just blocking social media buttons
def is_href_media(href):
    list_of_medias = ["facebook", "twitter", "instagram", "youtube"]

    for media in list_of_medias:
        if media in href:
            return True

    return False


def collect_titles_dynamic(session, NewsTable, URL):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        bad_parents = a_tag.find_parents(['header', 'footer'])
        if bad_parents:
            continue
        # Check the inner text of the <a> tag
        inner_text = a_tag.get_text().strip()
        if len(re.findall(r'\w+', inner_text)) > 3 and '@' not in inner_text:
            if is_href_media(a_tag['href'].strip()):
                continue
            link = {'text': inner_text, 'href': a_tag['href'].strip()}
            links.append(link)
        else:
            # Check the attribute values of the <a> tag
            for attr_name, attr_value in a_tag.attrs.items():
                if isinstance(attr_value, str) and attr_name != 'href':
                    if len(re.findall(r'\w+', attr_value)) > 3 and '@' not in attr_value:
                        if is_href_media(a_tag['href'].strip()):
                            continue
                        link = {'text': a_tag.get_text().strip(), 'href': a_tag['href'].strip()}
                        links.append(link)
                        break

    data = get_full_row(links, URL)

    writeTitles(data, session, NewsTable)
