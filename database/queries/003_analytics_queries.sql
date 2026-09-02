-- 1. Top songs by total streams
SELECT
    s.song_name,
    SUM(f.stream_count) AS total_streams
FROM fact_streaming f
JOIN dim_song s
    ON f.song_id = s.song_id
GROUP BY s.song_name
ORDER BY total_streams DESC;


-- 2. Top artists by total streams
SELECT
    a.artist_name,
    SUM(f.stream_count) AS total_streams
FROM fact_streaming f
JOIN dim_song s
    ON f.song_id = s.song_id
JOIN dim_artist a
    ON s.artist_id = a.artist_id
GROUP BY a.artist_name
ORDER BY total_streams DESC;


-- 3. Streams by country
SELECT
    c.country_name,
    SUM(f.stream_count) AS total_streams
FROM fact_streaming f
JOIN dim_country c
    ON f.country_id = c.country_id
GROUP BY c.country_name
ORDER BY total_streams DESC;


-- 4. Streams by genre
SELECT
    g.genre_name,
    SUM(f.stream_count) AS total_streams
FROM fact_streaming f
JOIN dim_song s
    ON f.song_id = s.song_id
JOIN dim_genre g
    ON s.genre_id = g.genre_id
GROUP BY g.genre_name
ORDER BY total_streams DESC;


-- 5. Artist + country performance
SELECT
    a.artist_name,
    c.country_name,
    SUM(f.stream_count) AS total_streams
FROM fact_streaming f
JOIN dim_song s
    ON f.song_id = s.song_id
JOIN dim_artist a
    ON s.artist_id = a.artist_id
JOIN dim_country c
    ON f.country_id = c.country_id
GROUP BY
    a.artist_name,
    c.country_name
ORDER BY total_streams DESC;