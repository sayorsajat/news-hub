import json
from http.server import SimpleHTTPRequestHandler
import os
from models.engine import Session
from models.news_model import NewsTable

class HTTPHandler(SimpleHTTPRequestHandler):
    @staticmethod
    def news_to_dict(news):
        # Convert a NewsTable object to a dictionary
        return {
            "id": news.id,
            "type": news.type,
            "title": news.title,
            "descriptionUrl": news.descriptionUrl,
            "content": str(news.content),
            "language": news.language,
            "source": news.source,
        }

    def do_GET(self):
        if self.path == "/news/getRecent":
            # Add CORS headers to allow cross-origin requests
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET")
            self.send_header("Content-Type", "application/json")
            self.send_response(200)  # Sent after headers
            self.end_headers()

            session = Session()
            # Query 50 recent rows from the NewsTable
            recent_news = session.query(NewsTable).order_by(NewsTable.id.desc()).limit(50).all()
            session.close()

            # Convert the list of NewsTable objects to a list of dictionaries
            response_data = [self.news_to_dict(news) for news in recent_news]
            response_json = json.dumps(response_data)
            self.wfile.write(response_json.encode("utf-8"))

        elif self.path == "/view/view.html":
            #print("Received GET request for /view/view.html")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # Read the view.html file and send it as the response
            with open(os.path.join(os.getcwd(), "view", "view.html"), "r") as f:
                self.wfile.write(f.read().encode())

        else:
            # For all other requests, serve files as static content
            return super().do_GET()