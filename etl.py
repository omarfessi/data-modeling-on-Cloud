from time import time
import configparser
import psycopg2 # to import the Postgresql python driver
from sql_queries import copy_table_queries, insert_table_queries # import SQL queries lists from sql_queries.py

def load_staging_tables(cur, conn):
    """
    Load the staging_tables by executing SQL copy commands 
    
    Parameters :
    cur  : Allows Python code to execute PostgreSQL command in a database session
    conn : The connection to the database
    
    Returns: 
    staging_events & song_events tables loaded with JSON data in the S3 Bucket 
    """
    for query in copy_table_queries:
    	t0=time()
    	cur.execute(copy_table_queries[query])
    	conn.commit()
    	copyTime=time()-t0
    	print(" {} is done in : {} sec\n".format(query,copyTime))

def insert_tables(cur, conn):
    """
    Insert the appropriate data int the final tables  by executing SQL insert commands 
    
    Parameters :
    cur  : Allows Python code to execute PostgreSQL command in a database session
    conn : The connection to the database
    
    Returns: 
    Dimensional& fact tables loaded with data from staging tables
    """
    for query in insert_table_queries:
    	t0=time()
    	cur.execute(insert_table_queries[query])
    	conn.commit()
    	copyTime=time()-t0
    	print(" {} is done in : {} sec\n".format(query,copyTime))

def main():
    """
    Initiate a configparser instance and read the configuration file 'redshift-configuration.cfg'
    Establich the connection to the postgres database in S3 by providing host, database name and credentials in 'redshift-configuration.cfg'
    Instanciate a cursor to allow Python code to execute PostgreSQL command in the database session
    Call load_staging_tables & insert_tables create above 
    Close the connection.
    

    """
    config = configparser.ConfigParser()
    config.read('redshift-configuration.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['DATABASE_CONFIGURATION'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

