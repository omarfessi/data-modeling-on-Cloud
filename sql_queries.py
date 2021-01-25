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


drop_table_queries=[staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,\
					 song_table_drop, artist_table_drop, time_table_drop]

create_table_queries=[staging_events_table_create,staging_songs_table_create, time_table_create, artist_table_create, \
					song_table_create, user_table_create, songplay_table_create]