import psycopg2

from config import database

def get_item(id: int):
    try:
        connection = psycopg2.connect(
            host = database['host'],
            user = database['user'],
            database = database['db_name']
        )

        connection.autocommit = True

        with connection.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS images(
                    id serial PRIMARY KEY,
                    filename varchar(255) NOT NULL,
                    filepath varchar(255) NOT NULL);
            """)

        

    except Exception as ex:
        print(ex)
        return -1
    finally:
        if connection:
            connection.close()

get_item(0)