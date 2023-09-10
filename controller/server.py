import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from models.engine import Session
from models.news_model import NewsTable
from sqlalchemy import or_, and_
from typing import List
from urgency_meter import measureUrgency


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


app = FastAPI()

app.mount("/view", StaticFiles(directory="view"), name="view")


@app.post("/news/getRecent")
async def get_recent_news(keywords: List[dict]):
    if not keywords:
        raise HTTPException(status_code=400, detail="No keywords provided")

    session = Session()

    # Create a list to hold the SQLAlchemy OR filter conditions
    filter_conditions = []

    # Iterate through the keywords and create filter conditions for each keyword
    for keyword_obj in keywords:
        keyword_condition = None

        # Iterate through the keyword_obj dictionary
        for keyword, weight in keyword_obj.items():
            # Create a filter condition for both title and content for the current keyword
            title_filter = NewsTable.title.ilike(f'%{keyword}%')
            content_filter = NewsTable.content.ilike(f'%{keyword}%')

            # Combine title and content filters for the current keyword using OR
            keyword_condition_for_current_keyword = or_(title_filter, content_filter)

            # Combine the condition for the current keyword with the overall keyword_condition
            if keyword_condition is None:
                keyword_condition = keyword_condition_for_current_keyword
            else:
                keyword_condition = or_(keyword_condition, keyword_condition_for_current_keyword)

        # Append the condition to the list of filter conditions
        if keyword_condition is not None:
            filter_conditions.append(keyword_condition)

    # Combine all filter conditions using OR
    combined_condition = None
    for condition in filter_conditions:
        if combined_condition is None:
            combined_condition = condition
        else:
            combined_condition = or_(combined_condition, condition)

    # Additional conditions: Ensure that content is not 'None'
    content_not_none_condition = NewsTable.content != 'None'

    # Combine all conditions using AND
    final_condition = and_(combined_condition, content_not_none_condition)

    # Query the NewsTable with the final condition and get all news
    recent_news = session.query(NewsTable).filter(final_condition).all()
    session.close()

    # Calculate urgency for each news item and store it in response_data
    response_data = []

    # Sort the news by urgency in descending order
    urgency_data = [(news, measureUrgency(news.title + "\n" + news.content, keywords)) for news in recent_news]
    urgency_data.sort(key=lambda x: x[1], reverse=True)

    # Get the two most urgent news items
    most_urgent_news = urgency_data[:2]

    for news, urgency in most_urgent_news:
        news_dict = news_to_dict(news)
        news_dict["urgency"] = urgency
        response_data.append(news_dict)

    # Convert the list of NewsTable objects to a list of dictionaries with urgency property
    response_json = jsonable_encoder(response_data)

    # Return the JSON response with urgency property
    return JSONResponse(content=response_json)


@app.put("/user/viewSettings", response_class=Response)
async def save_user_view_settings(html_fragment: str = Body(None, media_type="text/html")):
    # Path to the "user_view.html" file
    file_path = os.path.join("view", "user_view.html")

    # Check if the HTML fragment is None or empty
    if html_fragment is None or html_fragment.strip() == "":
        # If it's None or empty, clear the file by opening it in write mode with an empty string
        with open(file_path, "w") as file:
            file.write("")
    else:
        # If it's not empty, write the received HTML fragment to the file (create or overwrite)
        with open(file_path, "w") as file:
            file.write(html_fragment)

    return Response(status_code=200)
