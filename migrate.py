import pymysql
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MySQL connection using environment variables
mysql_conn = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

# PostgreSQL connection using environment variables
post_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    dbname=os.getenv("POSTGRES_DATABASE")
)

# Rest of your code remains the same
mysql_cursor = mysql_conn.cursor()
mysql_cursor.execute("SELECT * FROM tools")
data = mysql_cursor.fetchall()
columns = [desc[0] for desc in mysql_cursor.description]

post_cursor = post_conn.cursor()

drop_table_query = "DROP TABLE IF EXISTS tools_table"
post_cursor.execute(drop_table_query)
post_conn.commit()

create_table_query = """
CREATE TABLE tools_table (
    tool_name VARCHAR(45),
    tool_type VARCHAR(45),
    tool_use VARCHAR(45),
    tool_category VARCHAR(45)
)
"""
post_cursor.execute(create_table_query)
post_conn.commit()

placeholders = ', '.join(['%s'] * len(columns))
insert_query = f"INSERT INTO tools_table ({', '.join(columns)}) VALUES ({placeholders})"
post_cursor.executemany(insert_query, data)
post_conn.commit()

mysql_cursor.close()
mysql_conn.close()
post_cursor.close()
post_conn.close()
