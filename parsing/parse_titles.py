from time import sleep
from lib.constants import (
    delay_of_fetching_titles,
    parsingTitlesEnabled,
    classic_news_type,
    english_language_type
)
from csv import DictReader

from db_util.writeNews import writeTitles
from models.engine import Session
from models.news_model import NewsTable
from bs4 import BeautifulSoup
import re
import requests
from tld import get_fld
from tld.utils import update_tld_names


update_tld_names()


def getDescriptionUrl(URL, href):
    descriptionUrl = ""
    if "://" not in href:
        baseURL = create_base_url(URL)
        descriptionUrl = f"{baseURL}{href}"
    else:
        descriptionUrl = href
    return descriptionUrl


def create_base_url(full_url):
    return get_fld(full_url)


def get_full_rows(rows, URL, lang):
    data = []

    for row in rows:
        href = row["href"]

        descriptionUrl = getDescriptionUrl(URL, href)

        data.append({"type": classic_news_type, "title": row["text"], "descriptionUrl": descriptionUrl,
                     "content": None, "summary": row["summary"],"language": lang, "source": URL})

    return data


# just blocking social media buttons
def is_href_media(href):
    list_of_medias = ["facebook", "twitter", "instagram", "youtube"]

    for media in list_of_medias:
        if media in href:
            return True

    return False


def parse_titles(session, NewsTable, URL):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"}

    try:
        from lib.proxy import proxy
        page = requests.get(URL, headers=headers, proxies=proxy)
    except:
        page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    rows = []

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
            rows.append(link)
        else:
            # Check the attribute values of the <a> tag
            for attr_name, attr_value in a_tag.attrs.items():
                if isinstance(attr_value, str) and attr_name != 'href':
                    if len(re.findall(r'\w+', attr_value)) > 3 and '@' not in attr_value:
                        if is_href_media(a_tag['href'].strip()):
                            continue
                        link = {'text': a_tag.get_text().strip(), 'href': a_tag['href'].strip()}
                        rows.append(link)
                        break

    data = get_full_rows(rows, URL, english_language_type)

    writeTitles(data, session, NewsTable)
