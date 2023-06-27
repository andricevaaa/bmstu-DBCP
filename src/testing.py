import psycopg2
import time

# Establish a connection to the database
conn = psycopg2.connect(database="postgres", user="postgres", password="root", host="localhost")

# Create a cursor object
cur = conn.cursor()

# SQL query
sql_query1 = """
    SELECT oa.ordalbid, o.orderid, o.orderdate, o.ordertype, oa.username, a.albumname, a.albumver, g.pcname
    FROM ordalb oa
    INNER JOIN orders o ON oa.orderid = o.orderid
    INNER JOIN apg p ON oa.apg = p.apgid
    INNER JOIN album a ON p.albumid = a.albumid
    INNER JOIN gift g ON p.giftid = g.giftid
"""

sql_query2 = """
    SELECT *
    FROM ordalb oa
    INNER JOIN orders o ON oa.orderid = o.orderid
    INNER JOIN apg p ON oa.apg = p.apgid
    INNER JOIN album a ON p.albumid = a.albumid
    INNER JOIN gift g ON p.giftid = g.giftid
"""

timec = []
for i in range(100):
    # Measure the execution time
    start_time = time.time()

    # Execute the SQL query
    cur.execute(sql_query2)

    # Fetch the results if needed
    results = cur.fetchall()

    # Calculate the execution time
    execution_time = time.time() - start_time
    timec.append(execution_time)


# Print the execution time
print("Execution Time: ", sum(timec) / len(timec))

# Close the cursor and connection
cur.close()
conn.close()
