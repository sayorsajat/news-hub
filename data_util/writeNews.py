from sqlalchemy.dialects.postgresql import insert

def writeNews(rows, session, NewsTable):
    # Perform bulk insert, inserting only unique rows
    for row in rows:
        stmt = insert(NewsTable).values(**row).on_conflict_do_nothing(index_elements=['id'])
        session.execute(stmt)
    
    session.commit()