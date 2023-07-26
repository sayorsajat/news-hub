from sqlalchemy.dialects.postgresql import insert

def writeTitles(rows, session, NewsTable):
    # Perform bulk insert, inserting only unique rows
    for row in rows:
        stmt = insert(NewsTable).values(**row).on_conflict_do_nothing()
        session.execute(stmt)
    
    session.commit()

def writeDescription(description, row_id, session, NewsTable):
    # Find the row based on the row_id
    row_to_update = session.query(NewsTable).get(row_id)

    if row_to_update:
        row_to_update.content = description
        session.commit()
        print("Description successfully written to row!")
    else:
        print(f"Row with id: {row_id} not found!")
    
    session.commit()