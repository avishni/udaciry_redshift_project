# Udacity data engineering - Data Warehouse project

**Sparkify** is the next generation of music streaming app. As part of Sparkify project , data is being collected about the app usar activity including the song and the artist of each session. This data will be used for analytics, to make the app better and to improve business decisions.
Sample analytics questions

### Some questions that the data in this database can help to answer:
-	top artists by songs plays
-	top songs by plays
-	preferred songs by user gender
-	optional relation between songs listened (for recommendation system)  
-	number of songs played by weekday, and by season


## Dataset
The data set contains to data sources, both stores as json files in S3
1.	Song data – Each file is in JSON format and contains metadata about a song and the artist of that song
2.	Log data - activity logs from the music streaming app

## tables
### staging tables

# TBD
### analytics tables

**Fact Table**
1.	songplays - records in event data associated with song plays i.e. records with page NextSong 
      (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)

**Dimension Tables**
2.	users - users in the app
      (user_id, first_name, last_name, gender, level)
3.	songs - songs in music database
    (song_id, title, artist_id, year, duration)
4.	artists - artists in music database
    (artist_id, name, location, lattitude, longitude)
5.	time - timestamps of records in songplays broken down into specific units
    (start_time, hour, day, week, month, year, weekday)

# TBD

## Files in the project
- **Dwg.cfg** 	- configuration files
- **sql_queries.py** – python script to define the SQL queries for creating the tables and inserting date to the tables
- **create_tables.py** – python script to delete and create the tables in the database
- **etl.py** – script for the ETL process
- **Readme.md** – this documnatation file

## How to run

**Prerequisite**
A running instance of AWS redshift cluster (minimum 4 nodes is recommended)

1. update the *dwh.cfg* file
2. run *python create_tables.py* to create the tables
3. run *python etl.py* to copy the data from the source files to the staging tables and from the staging tables to the tables used for analytics
