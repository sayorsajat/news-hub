from data_util.writeNews import writeNews
from bs4 import BeautifulSoup
from lib.constants import classic_news_type, english_language
import re
import requests

def get_full_row(links, URL):
    data = []
    for link in links:
        href = link["href"]
        data.append({"type": classic_news_type, "title": link["text"], "descriptionUrl": f"{URL}{href}", 
                     "content": None, "language": english_language, "source": URL})

    return data


def collect_titles_dynamic(session, NewsTable, URL):

    page = requests.get(URL)
    
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
                if isinstance(attr_value, str):
                    if len(re.findall(r'\w+', attr_value)) > 3 and '|' not in attr_value and '/' not in attr_value:
                        link = {'text': a_tag.get_text().strip(), 'href': a_tag['href'].strip()}
                        links.append(link)
                        break  # Stop searching for other attributes if a valid one is found


    data = get_full_row(links, URL)

    writeNews(data, session, NewsTable)