from data_util.writeNews import writeDescription
from newspaper import Article, Config

def sanitize_text(text):
    # Remove null characters because they are crashing writing to database
    return ''.join(c for c in text if c.isprintable() or c.isspace())

def collect_description_dynamic(session, NewsTable, URL, ID):
    USER_AGENT = "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"
    config = Config()
    config.browser_user_agent = USER_AGENT

    try:
        article = Article(URL, config=config)

        article.download()
        article.parse()
    except:
        print("no access to url")
        writeDescription("error while collecting", ID, session, NewsTable)
    
    
    

    if(str(article.text)):
        writeDescription(str(article.text), ID, session, NewsTable)
    else:
        print(f"description is empty. Url: {URL}")
        writeDescription("error while collecting", ID, session, NewsTable)
