import feedparser
from urllib.request import ProxyHandler

import requests

from db_util.writeNews import writeTitles
from lib.constants import english_language_type
from parsing.parse_titles import get_full_rows, create_base_url


def parse_rss_headings(session, NewsTable, URL):
    UserAgent = "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"
    try:
        from lib.proxy import proxy

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"}

        page = requests.get(URL, headers=headers, proxies=proxy)

        feed = feedparser.parse(page.text)
    except:
        feed = feedparser.parse(URL, agent=UserAgent)

    rows = []
    for entry in feed.entries:
        # parsing url of article
        href = ""
        for link in entry.links:
            if link["type"] == "text/html" and href == "":
                href = link.href
        if href == "" and "type" not in entry['link']:
            if entry['link'] != "" and create_base_url(entry['link']) == create_base_url(URL):
                href = entry['link']

        # parsing summary of article
        summary = ""
        if "description" in entry.keys():
            summary = entry.description
        elif "summary" in entry.keys():
            summary = entry.summary

        rows.append({'text': entry.title,
                     'summary': summary,
                     'href': href.strip()})

    data = get_full_rows(rows, URL, english_language_type)

    writeTitles(data, session, NewsTable)
