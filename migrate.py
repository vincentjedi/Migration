import pymysql
import psycopg2

# Establishing MySQL connection
mysql_conn = pymysql.connect(
    host="localhost",
    user="root",
    passwd="vince123",
    database="magari"
)

# Establishing PostgreSQL connection
post_conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="vince123",
    dbname="cars"
)

# Fetching the data from MySQL database
mysql_cursor = mysql_conn.cursor()
mysql_cursor.execute("SELECT * FROM tools")
data = mysql_cursor.fetchall()
columns = [desc[0] for desc in mysql_cursor.description]

# Creating the same table in PostgreSQL
post_cursor = post_conn.cursor()

# Drop the table if it exists
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

# Inserting the data to the PostgreSQL table
placeholders = ', '.join(['%s'] * len(columns))
insert_query = f"INSERT INTO tools_table ({', '.join(columns)}) VALUES ({placeholders})"
post_cursor.executemany(insert_query, data)
post_conn.commit()

# Closing all the connections
mysql_cursor.close()
mysql_conn.close()
post_cursor.close()
post_conn.close()
