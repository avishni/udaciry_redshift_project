import configparser
import psycopg2
from sql_queries import copy_table_queries , insert_table_queries
import time


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        queryname = query.split("\n")[1][:-1].strip()
        print('running query: ' , queryname)
        t0 = time.time()
        cur.execute(query)
        conn.commit()
        loadTime = time.time()-t0
        print("=== DONE IN: {0:.2f} sec\n".format(loadTime))


def insert_tables(cur, conn):
    for query in insert_table_queries:
        queryname = query.split("(")[0].strip()
        print('running query: ' , queryname)
        t0 = time.time()
        cur.execute(query)
        conn.commit()
        loadTime = time.time()-t0
        print("=== DONE IN: {0:.2f} sec\n".format(loadTime))


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()