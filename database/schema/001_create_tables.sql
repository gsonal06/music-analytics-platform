-- =========================================
-- MUSIC ANALYTICS PLATFORM - STAR SCHEMA
-- =========================================

-- 1. Artist Dimension
CREATE TABLE dim_artist (
    artist_id INT PRIMARY KEY,
    artist_name VARCHAR(150) NOT NULL
);


-- 2. Genre Dimension
CREATE TABLE dim_genre (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL
);


-- 3. Country Dimension
CREATE TABLE dim_country (
    country_id INT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL
);


-- 4. Date Dimension
CREATE TABLE dim_date (
    date_id DATE PRIMARY KEY,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL
);


-- 5. Song Dimension
CREATE TABLE dim_song (
    song_id INT PRIMARY KEY,
    song_name VARCHAR(200) NOT NULL,
    artist_id INT NOT NULL,
    genre_id INT NOT NULL,
    release_date DATE,

    FOREIGN KEY (artist_id)
        REFERENCES dim_artist(artist_id),

    FOREIGN KEY (genre_id)
        REFERENCES dim_genre(genre_id)
);


-- 6. Streaming Fact Table
CREATE TABLE fact_streaming (
    stream_id BIGINT PRIMARY KEY,
    song_id INT NOT NULL,
    country_id INT NOT NULL,
    stream_date DATE NOT NULL,
    stream_count INT NOT NULL,

    FOREIGN KEY (song_id)
        REFERENCES dim_song(song_id),

    FOREIGN KEY (country_id)
        REFERENCES dim_country(country_id),

    FOREIGN KEY (stream_date)
        REFERENCES dim_date(date_id)
);