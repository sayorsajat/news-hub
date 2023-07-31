import threading
import csv
from http.server import HTTPServer
from time import sleep
from lib.constants import (
    delay_of_fetching_titles, 
    delay_of_fetching_content_between_same_source,
    web_server_port
    )
from lib.collect_titles import collect_titles_dynamic
from lib.collect_description import collect_description_dynamic
from models.news_model import NewsTable
from models.engine import Session
from controller.server import HTTPHandler

session = Session()

# async running server, so that it doesn't block further code
def run_server():
    server_address = ("", web_server_port)
    httpd = HTTPServer(server_address, HTTPHandler)
    print(f"Server running on port {web_server_port}...")
    httpd.serve_forever()

def gather():
    while True:
        with open("./lib/news_sources.csv", 'r') as file:
            csv_file = csv.DictReader(file, delimiter=';')
            websites_list = []
            for row in csv_file:
                if row["is_description_availaible"] == "yes":
                    websites_list.append(row["website"])
                collect_titles_dynamic(session, NewsTable, row["website"])
                print("collected titles")
                sleep(delay_of_fetching_titles)
                        

            #Basically, while there are news without content value
            while session.query(NewsTable).filter(NewsTable.content.is_(None), NewsTable.source.in_(websites_list)).all():
                # this loop is for fetching sources in special order, one description for each source in one cycle of loop
                # this creates non-artificial delay, so that program doesn't DDOS website and time is not wasted
                for website in websites_list:
                    # get one row without content from specific source
                    row = session.query(NewsTable).filter(NewsTable.content.is_(None), NewsTable.source == website).first()
                    if row:
                        collect_description_dynamic(session, NewsTable, row.descriptionUrl, row.id)
                        sleep(delay_of_fetching_content_between_same_source/len(websites_list))

            file.close()
        
        print("All news and descriptions collected!")
        sleep(240)

server_thread = threading.Thread(target=run_server)
server_thread.start()

gather_thread = threading.Thread(target=gather)
gather_thread.start()

server_thread.join()
gather_thread.join()

session.close()