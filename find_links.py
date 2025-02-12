import requests
from bs4 import BeautifulSoup as Soup
import os
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for the attributes to be extracted from the sitemap
ATTRS = ["loc", "lastmod", "priority"]

# Get sitemap URL and strip quotes if present
sitemap_url = os.getenv('SITEMAP_URL')
if sitemap_url:
    # Remove any surrounding quotes that might have been added in .env
    sitemap_url = sitemap_url.strip('"\'')
else:
    sitemap_url = 'https://docs.customgpt.ai/sitemap.xml'

def parse_sitemap(url, csv_filename="urls.csv"):
    """Parse the sitemap at the given URL and append the data to a CSV file."""
    if not url:
        return False

    print(f"Fetching sitemap from: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch sitemap. Status code: {response.status_code}")
        return False

    soup = Soup(response.content, "xml")

    # Recursively parse nested sitemaps
    for sitemap in soup.find_all("sitemap"):
        loc = sitemap.find("loc").text
        parse_sitemap(loc, csv_filename)

    root = os.path.dirname(os.path.abspath(__file__))
    urls = soup.find_all("url")

    rows = []
    for url in urls:
        row = []
        for attr in ATTRS:
            found_attr = url.find(attr)
            row.append(found_attr.text if found_attr else "n/a")
        rows.append(row)

    file_exists = os.path.isfile(os.path.join(root, csv_filename))

    with open(os.path.join(root, csv_filename), "a+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(ATTRS)
        writer.writerows(rows)

if __name__ == "__main__":
    print(f"Starting sitemap parse from: {sitemap_url}")
    parse_sitemap(sitemap_url)