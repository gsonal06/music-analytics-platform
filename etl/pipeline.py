from pathlib import Path
import pandas as pd
from sqlalchemy import text

from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql+psycopg://music_user:music_password@localhost:5432/music_analytics"

engine = create_engine(DATABASE_URL)


BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "music_streams.csv"
PROCESSED_FILE = BASE_DIR / "data" / "processed" / "valid_music_streams.csv"
REJECTED_FILE = BASE_DIR / "data" / "rejected" / "invalid_music_streams.csv"


def extract_data():
    return pd.read_csv(RAW_FILE)


def validate_data(df):

    valid_song_ids = {1, 2, 3, 4, 5, 6, 7, 8}
    valid_artist_ids = {1, 2, 3, 4, 5}

    valid = pd.Series(True, index=df.index)

    valid &= df["stream_count"].notna()
    valid &= df["stream_count"] > 0
    valid &= df["song_id"].isin(valid_song_ids)
    valid &= df["artist_id"].isin(valid_artist_ids)

    # Keep only the first occurrence of a duplicate stream_id
    valid &= ~df["stream_id"].duplicated(keep="first")

    valid_df = df[valid].copy()
    rejected_df = df[~valid].copy()

    return valid_df, rejected_df


def save_data(valid_df, rejected_df):

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    REJECTED_FILE.parent.mkdir(parents=True, exist_ok=True)

    valid_df.to_csv(PROCESSED_FILE, index=False)
    rejected_df.to_csv(REJECTED_FILE, index=False)

    print("Valid records:", len(valid_df))
    print("Rejected records:", len(rejected_df))


def transform_data():

    df = pd.read_csv(PROCESSED_FILE)

    # Convert dates to proper date format
    df["release_date"] = pd.to_datetime(df["release_date"]).dt.date
    df["stream_date"] = pd.to_datetime(df["stream_date"]).dt.date

    # Convert stream count from float to integer
    df["stream_count"] = df["stream_count"].astype(int)

    return df


def load_data(df):

    with engine.begin() as connection:

        # Load new dates into date dimension
        for date in df["stream_date"].unique():

            date = pd.Timestamp(date)

            connection.execute(
                text("""
                    INSERT INTO dim_date
                    (date_id, year, month, day, quarter)
                    VALUES
                    (:date_id, :year, :month, :day, :quarter)
                    ON CONFLICT (date_id) DO NOTHING
                """),
                {
                    "date_id": date.date(),
                    "year": date.year,
                    "month": date.month,
                    "day": date.day,
                    "quarter": date.quarter
                }
            )

        # Load streaming facts
        for _, row in df.iterrows():

            connection.execute(
                text("""
                    INSERT INTO fact_streaming
                    (stream_id, song_id, country_id, stream_date, stream_count)
                    VALUES
                    (:stream_id, :song_id, :country_id,
                     :stream_date, :stream_count)
                    ON CONFLICT (stream_id) DO NOTHING
                """),
                {
                    "stream_id": int(row["stream_id"]),
                    "song_id": int(row["song_id"]),
                    "country_id": get_country_id(row["country"]),
                    "stream_date": row["stream_date"],
                    "stream_count": int(row["stream_count"])
                }
            )

    print("Data loaded into PostgreSQL successfully!")


def get_country_id(country_name):

    country_ids = {
        "India": 1,
        "United States": 2,
        "United Kingdom": 3,
        "Canada": 4,
        "Australia": 5
    }

    return country_ids[country_name]


if __name__ == "__main__":

    df = extract_data()

    valid_df, rejected_df = validate_data(df)

    save_data(valid_df, rejected_df)

    transformed_df = transform_data()

    load_data(transformed_df)