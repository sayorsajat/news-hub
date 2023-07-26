import logging
from bs4 import BeautifulSoup
from data_util.writeNews import writeDescription
import re
import requests

def collect_description_dynamic(session, NewsTable, URL, ID):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    description = ""

    for p_tag in soup.find_all('p'):
        # Check if the parent tag is not <a>
        if p_tag.parent.name != 'a':
            # Check the inner text of the <p> tag
            inner_text = p_tag.get_text().strip()
            if len(re.findall(r'\w+', inner_text)) > 7 and '|' not in inner_text:
                description += f"\n{inner_text}"

    writeDescription(description, ID, session, NewsTable)