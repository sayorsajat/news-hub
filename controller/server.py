import json
import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models.engine import Session
from models.news_model import NewsTable
from sqlalchemy import or_, and_

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
async def get_recent_news(keywords: list[dict]):
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

    # Query the NewsTable with the final condition and get recent news
    recent_news = session.query(NewsTable).filter(final_condition) \
        .order_by(NewsTable.id.desc()).limit(50).all()
    session.close()

    # Convert the list of NewsTable objects to a list of dictionaries
    response_data = [news_to_dict(news) for news in recent_news]
    response_json = jsonable_encoder(response_data)
    return JSONResponse(content=response_json)

@app.put("/user/viewSettings", response_class=Response)
async def save_user_view_settings(html_fragment: str = Body(..., media_type="text/html")):
    # Path to the "user_view.html" file
    file_path = os.path.join("view", "user_view.html")

    # Write the received HTML fragment to the file (create or overwrite)
    with open(file_path, "w") as file:
        file.write(html_fragment)

    return Response(status_code=200)