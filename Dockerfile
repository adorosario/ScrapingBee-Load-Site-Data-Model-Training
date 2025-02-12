FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py ./

# Create a non-root user
RUN useradd -m -u 1000 scraper
RUN chown -R scraper:scraper /app
USER scraper

CMD ["/bin/bash"]
