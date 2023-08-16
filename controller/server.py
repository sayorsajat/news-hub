import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
import os
from models.engine import Session
from models.news_model import NewsTable


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

@app.get("/news/getRecent")
async def get_recent_news():
    session = Session()
    # Query 50 recent rows from the NewsTable
    recent_news = session.query(NewsTable).order_by(NewsTable.id.desc()).limit(50).all()
    session.close()

    # Convert the list of NewsTable objects to a list of dictionaries
    response_data = [news_to_dict(news) for news in recent_news]
    response_json = jsonable_encoder(response_data)
    return JSONResponse(content=response_json)