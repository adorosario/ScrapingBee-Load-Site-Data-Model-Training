import requests
from bs4 import BeautifulSoup as Soup
import os
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants for the attributes to be extracted from the sitemap
ATTRS = ["loc", "lastmod", "priority"]
SITEMAP_URL = os.getenv('SITEMAP_URL', 'https://docs.customgpt.ai/sitemap.xml')

def parse_sitemap(url, csv_filename="urls.csv"):
    """Parse the sitemap at the given URL and append the data to a CSV file."""
    if not url:
        return False

    response = requests.get(url)
    if response.status_code != 200:
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
    print(f"Starting sitemap parse from: {SITEMAP_URL}")
    parse_sitemap(SITEMAP_URL)