from csv import DictReader

from db_util.writeNews import writeDescription
from newspaper import Article, Config
from models.engine import Session
from models.news_model import NewsTable
from time import sleep
from lib.constants import (
    delay_of_fetching_content_from_same_source
)
from parsing.parse_titles import create_base_url

session = Session()


def sanitize_text(text):
    # Remove null characters because they are crashing writing to database
    return ''.join(c for c in text if c.isprintable() or c.isspace())


def collect_descriptions():
    with open("./lib/RSSList.csv", 'r') as file:
        csv_file = DictReader(file, delimiter=';')
        websites_list = []
        for row in csv_file:
            websites_list.append(row["website"])

        print(websites_list)

        # Basically, while there are news without content value
        while session.query(NewsTable).filter(NewsTable.content.is_(None), NewsTable.source.in_(websites_list)).all():
            # this loop is for fetching sources in special order, one description for each source in one cycle of loop
            # this creates non-artificial delay, so that program doesn't DDOS website and time is not wasted
            for website in websites_list:
                # get one row without content from specific source
                row = session.query(NewsTable).filter(NewsTable.content.is_(None), NewsTable.source == website).first()
                if row:
                    collect_description_dynamic(row.descriptionUrl, row.id)
                    sleep(delay_of_fetching_content_from_same_source / len(websites_list))
                    print('description collected')

        file.close()


def collect_description_dynamic(URL, ID):
    USER_AGENT = "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"
    config = Config()
    config.browser_user_agent = USER_AGENT
    try:
        from lib.proxy import proxy
        config.proxies = proxy
    except:
        pass

    article = Article(URL, config=config)

    try:
        article.download()
        article.parse()
    except:
        print("no access to url")
        writeDescription("error while collecting", ID, session, NewsTable)

    if str(article.text):
        writeDescription(str(article.text), ID, session, NewsTable)
    else:
        print(f"description is empty. Url: {URL}")
        writeDescription("error while collecting", ID, session, NewsTable)
