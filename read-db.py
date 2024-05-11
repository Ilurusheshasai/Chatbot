import sqlite3

# Connect to the database
conn = sqlite3.connect("scraped_data.db")
c = conn.cursor()

# Query the database to fetch all rows from the scraped_data table
c.execute("SELECT * FROM scraped_data")
rows = c.fetchall()

# Print the data
for row in rows:
    print(f"ID: {row[0]}, Heading: {row[1]}")

# Close the database connection
conn.close()
