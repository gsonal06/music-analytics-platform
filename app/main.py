from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text

from app.database import engine


app = FastAPI(title="Music Analytics API")


class StreamData(BaseModel):
    stream_id: int
    song_id: int
    country_id: int
    stream_date: str
    stream_count: int


@app.get("/")
def home():
    return {"message": "Music Analytics API is running"}


# -------------------------
# Ingestion API
# -------------------------

@app.post("/ingest")
def ingest_stream(data: StreamData):

    if data.stream_count <= 0:
        raise HTTPException(
            status_code=400,
            detail="stream_count must be greater than 0"
        )

    try:
        with engine.begin() as connection:

            connection.execute(
                text("""
                    INSERT INTO fact_streaming
                    (stream_id, song_id, country_id, stream_date, stream_count)
                    VALUES
                    (:stream_id, :song_id, :country_id,
                     :stream_date, :stream_count)
                """),
                {
                    "stream_id": data.stream_id,
                    "song_id": data.song_id,
                    "country_id": data.country_id,
                    "stream_date": data.stream_date,
                    "stream_count": data.stream_count
                }
            )

        return {
            "message": "Stream data ingested successfully",
            "stream_id": data.stream_id
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not insert stream data"
        )


# -------------------------
# Analytics APIs
# -------------------------

@app.get("/analytics/top-songs")
def top_songs(limit: int = 10, offset: int = 0):

    if limit <= 0:
        raise HTTPException(
            status_code=400,
            detail="limit must be greater than 0"
        )

    if offset < 0:
        raise HTTPException(
            status_code=400,
            detail="offset cannot be negative"
        )

    query = text("""
        SELECT
            s.song_name,
            SUM(f.stream_count) AS total_streams
        FROM fact_streaming f
        JOIN dim_song s
            ON f.song_id = s.song_id
        GROUP BY s.song_id, s.song_name
        ORDER BY total_streams DESC
        LIMIT :limit
        OFFSET :offset
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "limit": limit,
                "offset": offset
            }
        )

        return [
            {
                "song": row.song_name,
                "total_streams": row.total_streams
            }
            for row in result
        ]


@app.get("/analytics/top-artists")
def top_artists():

    query = text("""
        SELECT
            a.artist_name,
            SUM(f.stream_count) AS total_streams
        FROM fact_streaming f
        JOIN dim_song s
            ON f.song_id = s.song_id
        JOIN dim_artist a
            ON s.artist_id = a.artist_id
        GROUP BY a.artist_id, a.artist_name
        ORDER BY total_streams DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "artist": row.artist_name,
                "total_streams": row.total_streams
            }
            for row in result
        ]


@app.get("/analytics/top-genres")
def top_genres():

    query = text("""
        SELECT
            g.genre_name,
            SUM(f.stream_count) AS total_streams
        FROM fact_streaming f
        JOIN dim_song s
            ON f.song_id = s.song_id
        JOIN dim_genre g
            ON s.genre_id = g.genre_id
        GROUP BY g.genre_id, g.genre_name
        ORDER BY total_streams DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "genre": row.genre_name,
                "total_streams": row.total_streams
            }
            for row in result
        ]


@app.get("/analytics/countries")
def country_performance():

    query = text("""
        SELECT
            c.country_name,
            SUM(f.stream_count) AS total_streams
        FROM fact_streaming f
        JOIN dim_country c
            ON f.country_id = c.country_id
        GROUP BY c.country_id, c.country_name
        ORDER BY total_streams DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "country": row.country_name,
                "total_streams": row.total_streams
            }
            for row in result
        ]


@app.get("/analytics/trends")
def streaming_trends():

    query = text("""
        SELECT
            f.stream_date,
            SUM(f.stream_count) AS total_streams
        FROM fact_streaming f
        GROUP BY f.stream_date
        ORDER BY f.stream_date
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        return [
            {
                "date": str(row.stream_date),
                "total_streams": row.total_streams
            }
            for row in result
        ]