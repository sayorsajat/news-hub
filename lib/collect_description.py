from data_util.writeNews import writeDescription
import requests
from bs4 import BeautifulSoup
import gensim
from gensim.summarization import summarize

def sanitize_text(text):
    # Remove null characters because they are crashing writing to database
    return ''.join(c for c in text if c.isprintable() or c.isspace())

def collect_description_dynamic(session, NewsTable, URL, ID):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0"}

    page = requests.get(URL, headers=headers)
    
    soup = BeautifulSoup(page.content, 'html.parser')

    try:
        article_text = soup.get_text()
    except:
        print("no access to url")
        writeDescription("error while collecting", ID, session, NewsTable)
    
    
    

    if(str(article_text)):
        writeDescription(str(article_text), ID, session, NewsTable)
    else:
        print(f"description is empty. Url: {URL}")
        writeDescription("error while collecting", ID, session, NewsTable)
