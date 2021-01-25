import configparser
# initiate a configparser instance and read the file 'dwh.cfg'
config = configparser.ConfigParser()
config.read('redshift-configuration.cfg')

# DROP TABLES if they already exist
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop  = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop       = "DROP TABLE IF EXISTS songplays ;"
user_table_drop           = "DROP TABLE IF EXISTS users; "
song_table_drop           = "DROP TABLE IF EXISTS songs; "
artist_table_drop         = "DROP TABLE IF EXISTS artists; "
time_table_drop           = "DROP TABLE IF EXISTS time; "

drop_table_queries=[staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,\
				    song_table_drop, artist_table_drop, time_table_drop]

#CREATE TABLES 	
staging_events_table_create = ("""CREATE TABLE IF NOT EXISTS staging_events (
artist           varchar,
auth             varchar,
firstName        varchar, 
gender           varchar,
itemInSession    integer,
lastName         varchar,
length           float  ,
level            varchar,
location         varchar,
method           varchar,
page             varchar,
registration     bigint ,
sessionId        integer,
song             varchar, 
status           integer,
ts               bigint , 
userAgent        varchar,
userId           integer)
""")

staging_songs_table_create  = ("""CREATE TABLE IF NOT EXISTS staging_songs (
song_id          varchar,
num_songs        integer,
title            varchar,
artist_name      varchar,
artist_latitude  float  ,
year             integer,
duration         float  , 
artist_id        varchar,
artist_longitude float  ,
artist_location  varchar )
""")


songplay_table_create  =(""" CREATE TABLE IF NOT EXISTS songplays (
songplay_id   bigint identity(0,1),
start_time    timestamp REFERENCES time(start_time),
user_id       integer   REFERENCES users (user_id),
level         varchar   NOT NULL,
song_id       varchar   REFERENCES songs (song_id),
artist_id     varchar   REFERENCES artists(artist_id),
session_id    integer   NOT NULL, 
location      varchar   NOT NULL, 
user_agent    varchar   NOT NULL)
diststyle all;
""")

user_table_create = (""" CREATE TABLE IF NOT EXISTS users (
user_id    integer PRIMARY KEY,
first_name varchar,
last_name  varchar,
gender     varchar ,
level      varchar ) 
diststyle all;
""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS songs (
song_id   varchar PRIMARY KEY, 
title     varchar,
artist_id varchar ,
year      integer,
duration  decimal)
""")

artist_table_create =("""CREATE TABLE IF NOT EXISTS artists (
artist_id        varchar PRIMARY KEY,
artist_name      varchar ,
location         varchar ,
artist_latitude  float, 
artist_longitude float)
""")

time_table_create = (""" CREATE TABLE IF NOT EXISTS time (
start_time timestamp PRIMARY KEY,
hour       integer,
day        integer,
week       integer,
month      integer,
year       integer,
weekday    integer)
""")

# Copy staging events & songs data from an S3 bucket to staging tables

staging_events_copy=(""" 
copy staging_events from {} 
iam_role '{}'
format as json {} ;""").format(config['S3']['LOG_DATA'],config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
copy staging_songs from {} 
iam_role '{}'
format as json 'auto' ;""").format(config['S3']['SONG_DATA'],config['IAM_ROLE']['ARN'])

# Insert data into the star schema tables

songplay_table_insert=("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT DISTINCT '1970-01-01':: DATE + (se.ts/1000) * interval '1 second' AS start_time,
                se.userId   ,
                se.level    ,  
                ss.song_id  ,
                ss.artist_id,
                se.sessionId,
                se.location ,
                se.userAgent
FROM staging_events AS se JOIN staging_songs AS ss ON (ss.title=se.song AND ss.artist_name=se.artist)  
WHERE se.page = 'NextSong';""")

user_table_insert = ("""
INSERT INTO users 
SELECT DISTINCT userId   ,  
                firstName ,
                lastName  ,
                gender    ,
                level      
                
FROM staging_events 
WHERE userId IS NOT NULL;""")




song_table_insert = ("""
INSERT INTO songs 
SELECT DISTINCT song_id,
                title  ,
                artist_id,
                year,
                duration
FROM staging_songs""")

artist_table_insert =("""
INSERT INTO artists 
SELECT DISTINCT artist_id,
                artist_name,
                artist_location,
                artist_latitude,
                artist_longitude
                
FROM staging_songs;""")

time_table_insert=("""
INSERT INTO time 
SELECT DISTINCT '1970-01-01'::date + (ts/1000) * interval '1 second' AS start_time,
                EXTRACT ( hour    FROM start_time),
                EXTRACT ( day     FROM start_time),
                EXTRACT ( week    FROM start_time),
                EXTRACT ( month   FROM start_time),
                EXTRACT ( year    FROM start_time),
                EXTRACT ( weekday FROM start_time)
                
FROM staging_events """)



drop_table_queries  = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,song_table_drop, artist_table_drop, time_table_drop]

create_table_queries = [staging_events_table_create,staging_songs_table_create, time_table_create, artist_table_create, song_table_create, user_table_create, songplay_table_create]
copy_table_queries   = {'copying_staging_events':staging_events_copy, 'copying_staging_songs':staging_songs_copy}
insert_table_queries = {'inserting_user_table':user_table_insert,'inserting_song_table' :song_table_insert,'inserting_artist_table':artist_table_insert, 'inserting_time_table':time_table_insert, 'inserting_songplay_table':songplay_table_insert}

