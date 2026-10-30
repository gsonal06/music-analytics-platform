# Music Analytics Platform

A backend-focused music streaming analytics platform built using Python, Pandas, FastAPI and PostgreSQL.

## Architecture

```mermaid
flowchart TD
    A[CSV Dataset] --> B[Pandas ETL Pipeline]
    B --> C[Data Validation and Cleaning]
    C --> D[PostgreSQL Star Schema]
    D --> E[SQL Analytics]
    E --> F[FastAPI]
    F --> G[JSON Responses]

    H[Docker Compose] -.-> D
    H -.-> F

## Features

- CSV-based ETL pipeline
- Data validation and cleaning
- Duplicate and invalid record detection
- Rejected-data handling
- PostgreSQL star schema
- SQL analytical queries
- Stream ingestion API
- Analytics APIs
- API pagination
- Pytest API tests
- Dockerized application and database

## Database

The PostgreSQL database uses a star schema.

### Dimension Tables

- dim_artist
- dim_song
- dim_genre
- dim_country
- dim_date

### Fact Table

- fact_streaming

The fact table stores streaming events, while dimension tables store descriptive information about songs, artists, genres, countries and dates.

## ETL Pipeline

The ETL pipeline:

1. Extracts raw CSV data using Pandas.
2. Validates missing values, duplicates, IDs and stream counts.
3. Separates valid and rejected records.
4. Transforms dates and numeric fields.
5. Loads the processed data into PostgreSQL.

## API Endpoints

### Ingestion

POST `/ingest`

Adds a new streaming record.

### Analytics

GET `/analytics/top-songs`

GET `/analytics/top-artists`

GET `/analytics/top-genres`

GET `/analytics/countries`

GET `/analytics/trends`

## Technologies

- Python
- Pandas
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Pytest

## Running the Project

Start the application using Docker Compose:

```bash
docker compose up -d
