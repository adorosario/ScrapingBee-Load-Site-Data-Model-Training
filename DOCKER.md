# Docker Setup for Web Scraping Project

Simple setup for scraping website content using Docker.

## Quick Start

1. Copy the example env file and add your API key:
```bash
cp .env.example .env
# Edit .env and add your ScrapingBee API key
```

2. Build and start the container:
```bash
docker compose up -d --build
```

3. Enter the container:
```bash
docker compose exec scraper bash
```

4. Run the scrapers:
```bash
# First collect all URLs
python find_links.py

# Then extract the content
python extract_data.py
```

## Additional Information

### Files Generated
- `urls.csv`: Contains all URLs found in the sitemap
- `extracted_texts.txt`: Contains the extracted content

### Environment Variables
- `SCRAPINGBEE_API_KEY`: Your ScrapingBee API key
- `SITEMAP_URL`: URL of the sitemap (defaults to https://docs.customgpt.ai/sitemap.xml)

### Stopping the Container
```bash
docker compose down
```

### Using ScrapingBee
The code currently uses direct requests. To use ScrapingBee:
1. Make sure you have added your API key to .env
2. In extract_data.py, uncomment the ScrapingBee section in fetch_with_retry()