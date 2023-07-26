import json
from http.server import SimpleHTTPRequestHandler
from models.engine import Session
from models.news_model import NewsTable

class HTTPHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/news/getRecent":
            print("Received GET request for /news/getRecent")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            # Add CORS headers to allow cross-origin requests
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

            session = Session()
            # Query 50 recent rows from the NewsTable
            recent_news = session.query(NewsTable).order_by(NewsTable.id.desc()).limit(50).all()
            session.close()

            # Convert the list of NewsTable objects to a list of dictionaries
            response_data = [news_to_dict(news) for news in recent_news]
            self.wfile.write(json.dumps(response_data).encode())
        else:
            # For all other requests, serve files as static content
            return super().do_GET()

def news_to_dict(news):
    # Convert a NewsTable object to a dictionary
    return {
        "id": news.id,
        "type": news.type,
        "title": news.title,
        "descriptionUrl": news.descriptionUrl,
        "content": news.content,
        "language": news.language,
        "source": news.source,
    }