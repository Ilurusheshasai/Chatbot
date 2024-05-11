import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3

# URL of the website to scrape
url = "https://umbc.edu/about"

# Database connection
conn = sqlite3.connect("scraped_data.db")
c = conn.cursor()

# Create a table to store scraped data
c.execute('''CREATE TABLE IF NOT EXISTS scraped_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT, heading TEXT)''')

# Function to scrape the website
def scrape_website():
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find all the elements you want to scrape
            # For example, let's find all the <h1> elements
            headings = soup.find_all("h1")

            # Store the scraped data in the database
            for heading in headings:
                c.execute("INSERT INTO scraped_data (heading) VALUES (?)", (heading.text,))
                conn.commit()

            # Implement rate-limiting
            time.sleep(random.uniform(2, 5))  # Wait for 2-5 seconds between requests

        else:
            print(f"Error: {response.status_code}")
            # Implement error handling and retries
            if response.status_code == 429:  # Too many requests
                time.sleep(60)  # Wait for 1 minute before retrying
                scrape_website()
            elif response.status_code >= 500:  # Server error
                time.sleep(10)  # Wait for 10 seconds before retrying
                scrape_website()

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        # Implement error handling and retries
        time.sleep(10)  # Wait for 10 seconds before retrying
        scrape_website()

# Call the scrape_website function
scrape_website()

# Close the database connection
conn.close()
