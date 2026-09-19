CREATE INDEX IF NOT EXISTS idx_fact_song_id
ON fact_streaming(song_id);

CREATE INDEX IF NOT EXISTS idx_fact_country_id
ON fact_streaming(country_id);

CREATE INDEX IF NOT EXISTS idx_fact_stream_date
ON fact_streaming(stream_date);