import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE staging_events (
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender VARCHAR,
        itemInSession INT,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location VARCHAR,
        methos VARCHAR,
        page VARCHAR,
        registaration BIGINT,
        sessionId INT,
        song VARCHAR,
        status INT,
        ts BIGINT,
        userAgent VARCHAR,
        userId VARCHAR
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE staging_songs (
        num_songs INT,
        artist_id VARCHAR,
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR,
        title VARCHAR,
        duration FLOAT,
        year INT
    )
""")

songplay_table_create = ("""
    CREATE TABLE songplays(
        songplay_id INT, 
        start_time INT, 
        user_id VARCHAR, 
        level VARCHAR, 
        song_id VARCHAR, 
        artist_id VARCHAR, 
        session_id INT, 
        location VARCHAR, 
        user_agent VARCHAR
    )
""")

user_table_create = ("""
    CREATE TABLE users(
        user_id VARCHAR NOT NULL PRIMARY KEY,
        first_name VARCHAR NOT NULL, 
        last_name VARCHAR NOT NULL, 
        gender CHAR, 
        level VARCHAR NOT NULL
    )
""")

song_table_create = ("""
    CREATE TABLE songs(
        song_id VARCHAR NOT NULL PRIMARY KEY,
        title VARCHAR NOT NULL, 
        artist_id VARCHAR NOT NULL, 
        year INT, 
        duration FLOAT
    )
""")

artist_table_create = ("""
    CREATE TABLE artists(
        artist_id VARCHAR NOT NULL PRIMARY KEY,
        name VARCHAR,
        location VARCHAR, 
        lattitude FLOAT, 
        longitude FLOAT
    )
""")

time_table_create = ("""
    CREATE TABLE time(
        start_time TIMESTAMP NOT NULL,
        hour INT NOT NULL, 
        day INT NOT NULL, 
        week INT NOT NULL, 
        month INT NOT NULL, 
        year INT NOT NULL, 
        weekday INT NOT NULL
    )
""")

# STAGING TABLES
#
staging_events_copy = ("""
    COPY staging_events
    FROM {}
    IAM_ROLE {}
    JSON {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
     COPY staging_songs
     FROM {}
     IAM_ROLE {}
     JSON 'auto' truncatecolumns;
 """).format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN'])
# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT TIMESTAMP 'epoch' + (ts / 1000) * INTERVAL '1 Second ',
           user_id,
           level,
           song_id,
           artist_id,
           session_id,
           location,
           user_agent
    FROM staging_events events
    JOIN staging_songs songs ON (events.song = songs.title AND events.artist = songs.artist_name)
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT (user_id),
           first_name,
           last_name,
           gender,
           level
    FROM staging_events
    WHERE user_id IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT(song_id),
           title,
           artist_id,
           year,
           duration 
    FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT (artist_id),
           artist_name,
           artist_location,
           artist_latitude,
           artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT (TIMESTAMP 'epoch' + (ts / 1000) * INTERVAL '1 Second ') as ts_timestamp,
           EXTRACT(HOUR FROM ts_timestamp),
           EXTRACT(DAY FROM ts_timestamp),
           EXTRACT(WEEK FROM ts_timestamp),
           EXTRACT(MONTH FROM ts_timestamp),
           EXTRACT(YEAR FROM ts_timestamp),
           EXTRACT(DOW FROM ts_timestamp)
    FROM staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
