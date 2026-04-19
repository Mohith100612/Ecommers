import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    try:
        # Using the credentials from the updated .env
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Mohith6757*',
            host='localhost',
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ecommers'")
        exists = cur.fetchone()
        
        if not exists:
            print("Creating database 'ecommers'...")
            cur.execute("CREATE DATABASE ecommers")
            print("Database created.")
        else:
            print("Database 'ecommers' already exists.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error checking/creating database: {e}")

if __name__ == "__main__":
    create_database()
