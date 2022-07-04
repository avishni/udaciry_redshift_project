import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries
import time


def drop_tables(cur, conn):
    for query in drop_table_queries:
        queryname = query.strip()
        print('running query : ' , queryname)
        t0 = time.time()
        cur.execute(query)
        conn.commit()
        loadTime = time.time()-t0
        print("=== DONE IN: {0:.2f} sec\n".format(loadTime))


def create_tables(cur, conn):
    for query in create_table_queries:
        queryname = query.split("\n")[1][:-1].strip()
        print('running query : ' , queryname)
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

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()