import configparser
import psycopg2 # to import the Postgresql python driver
from sql_queries import create_table_queries, drop_table_queries # import SQL queries lists from sql_queries.py

def drop_tables(cur, conn):
    """
    Drop any tables if they exist 
    
    Parameters :
    cur  : Allows Python code to execute PostgreSQL command in a database session
    conn : The connection to the database
    
    
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

def create_tables(cur, conn):
    """
    CREATE both the songs and logs staging tables and each of the five tables with the right data types and conditions.
    
    
    Parameters :
    cur  : Allows Python code to execute PostgreSQL command in a database session
    conn : The connection to the database
    
    Returns: 
    Dimensional& fact tables created
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
def main():
	"""
    Initiate a configparser instance and read the configuration file 'redshift-configuration.cfg'
    Establich the connection to the postgres database in Redshift by providing host, database name and credentials in 'redshift-configuration.cfg'
    Instanciate a cursor to allow Python code to execute PostgreSQL command in the database session
    Call drop_tables and create_tables defined above 
    Close the connection.
    """
    config=configparser.configParser()
    config.read_file('redshift-configuration.cfg')
    conn=psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur=conn.cursor()
    drop_tables(cur, conn)
    create_tables(cur, conn)
    conn.close()
if __name__='__main__':
	main()

