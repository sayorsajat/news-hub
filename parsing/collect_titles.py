from time import sleep
from lib.constants import (
    delay_of_fetching_titles,
    parsingTitlesEnabled,
)
from csv import DictReader

from models.engine import Session
from models.news_model import NewsTable
from parsing.parse_rss_titles import parse_rss_headings
from parsing.parse_titles import parse_titles


def collect_headings():
    session = Session()
    with open("./lib/RSSList.csv", 'r') as file:
        csv_file = DictReader(file, delimiter=';')
        for row in csv_file:
            parse_rss_headings(session, NewsTable, row["website"])

            print("collected titles")
            sleep(delay_of_fetching_titles)

        file.close()

    if parsingTitlesEnabled:
        with open("./lib/news_sources.csv", 'r') as file:
            csv_file = DictReader(file, delimiter=';')
            for row in csv_file:
                if row["is_description_availaible"] == "yes":
                    parse_titles(session, NewsTable, row["website"])

                print("collected titles")
                sleep(delay_of_fetching_titles)

            file.close()
