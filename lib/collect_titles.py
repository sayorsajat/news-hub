import time
from data_util.writeNews import writeTitles
from bs4 import BeautifulSoup
from lib.constants import classic_news_type, english_language
import re
import requests

def getDescriptionUrl(URL, href):
    descriptionUrl = ""
    if not URL.endswith("/"):
        URL = URL + '/' 
    if(href.startswith("http")):
        descriptionUrl = f"{href}"
    else:
        descriptionUrl = f"{URL}{href}"
    return descriptionUrl

def get_full_row(links, URL):
    data = []
    
    for link in links:
        href = link["href"]

        descriptionUrl = getDescriptionUrl(URL, href)
        
        
        data.append({"type": classic_news_type, "title": link["text"], "descriptionUrl": descriptionUrl, 
                     "content": None, "language": english_language, "source": URL})

    return data


def collect_titles_dynamic(session, NewsTable, URL):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"}

    page = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    links = []

    for a_tag in soup.find_all('a', href=True):
        # Check the inner text of the <a> tag
        inner_text = a_tag.get_text().strip()
        if len(re.findall(r'\w+', inner_text)) > 3 and '|' not in inner_text and '/' not in inner_text:
            link = {'text': inner_text, 'href': a_tag['href'].strip()}
            links.append(link)
        else:
            # Check the attribute values of the <a> tag
            for attr_name, attr_value in a_tag.attrs.items():
                if isinstance(attr_value, str) and attr_name != 'href':
                    if len(re.findall(r'\w+', attr_value)) > 3 and '|' not in attr_value and '/' not in attr_value:
                        link = {'text': a_tag.get_text().strip(), 'href': a_tag['href'].strip()}
                        links.append(link)
                        break


    data = get_full_row(links, URL)

    writeTitles(data, session, NewsTable)