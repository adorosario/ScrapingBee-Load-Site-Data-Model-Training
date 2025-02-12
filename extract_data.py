import pandas as pd
import requests
from bs4 import BeautifulSoup
from scrapingbee import ScrapingBeeClient
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load URLs from CSV
df = pd.read_csv("urls.csv")
urls = df["loc"].tolist()

# Initialize ScrapingBee client with API key from env
api_key = os.getenv('SCRAPINGBEE_API_KEY')
if not api_key:
    raise ValueError("SCRAPINGBEE_API_KEY not found in environment variables")

client = ScrapingBeeClient(api_key=api_key)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_with_retry(url):
    """Fetch the URL with retries."""
    # Uncomment to use ScrapingBee
    # response = client.get(
    #     url,
    #     params={
    #         'premium_proxy': True,
    #         'country_code': 'gb',
    #         "block_resources": True,
    #         'device': 'desktop',
    #     }
    # )
    response = requests.get(url)
    response.raise_for_status()
    return response

def extract_text_from_url(url):
    print(f"Processing {url}")
    try:
        response = fetch_with_retry(url)
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""

def main():
    all_texts = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(extract_text_from_url, url): url for url in urls}

        for future in as_completed(futures):
            result = future.result()
            all_texts.append(result)

    with open("extracted_texts.txt", "w", encoding="utf-8") as file:
        for text in all_texts:
            file.write(text + "\n\n")

    print("Text extraction completed successfully!")

if __name__ == "__main__":
    main()