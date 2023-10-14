import threading
from time import sleep
from lib.constants import (
    update_news_database_delay,
    web_server_port,
    web_server_host
    )
from parsing.collect_titles import collect_headings
from parsing.collect_description import collect_descriptions
from models.engine import Session
from controller.server import app
import uvicorn

session = Session()


# async running server, so that it doesn't block further code
def run_server():
    uvicorn.run(app, port=web_server_port, host=web_server_host)
    print(f"Server running on port {web_server_port}...")


def gather():
    while True:
        collect_descriptions()

        collect_headings()

        collect_descriptions()

        print("All news and descriptions collected!")
        sleep(update_news_database_delay*60)


server_thread = threading.Thread(target=run_server)
server_thread.start()

gather_thread = threading.Thread(target=gather)
gather_thread.start()

server_thread.join()
gather_thread.join()

session.close()