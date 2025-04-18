# Lowes Web Scraper

A Python-based web scraper for extracting product information from Lowes.com based on a hierarchical category structure.

## Overview

This tool allows you to scrape product information from Lowes.com by navigating through a pre-defined structure of categories and pages. The scraper is designed to be respectful of Lowes' servers by implementing random delays between requests and rotating user agents.

## Features

- Hierarchical scraping structure defined in JSON
- Configurable request delays to prevent rate limiting
- Rotating user agents
- Comprehensive logging
- Recursive navigation through category pages
- JSON output format for easy data processing

## Requirements

- Python 3.6+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Define your scraping structure in `pages.json`. The file should have the following format:

```json
{
    "name": "home",
    "url": "https://www.lowes.com",
    "categories": [
        {
            "name": "Category1",
            "url": "https://www.lowes.com/c/Category1",
            "categories": [
                {
                    "name": "Subcategory1",
                    "url": "https://www.lowes.com/pl/Subcategory1"
                }
            ]
        }
    ]
}
```

2. Run the scraper:

```bash
python lowes_scraper.py
```

3. The results will be saved to `lowes_scraping_results.json`

## Configuration

You can modify the scraper's behavior by adjusting the values in the `LowesScraperConfig` class:

- `USER_AGENTS`: List of user agent strings to rotate through
- `DELAY_MIN`: Minimum delay between requests (in seconds)
- `DELAY_MAX`: Maximum delay between requests (in seconds)

## Output Format

The scraper produces a JSON file with the following structure:

```json
{
    "timestamp": "YYYY-MM-DD HH:MM:SS",
    "total_pages": X,
    "results": [
        {
            "name": "Page Name",
            "url": "https://www.lowes.com/...",
            "products": [
                {
                    "title": "Product Title",
                    "price": "$XX.XX",
                    "image": "https://...",
                    "url": "https://www.lowes.com/..."
                }
            ],
            "scraped_at": "YYYY-MM-DD HH:MM:SS"
        }
    ]
}
```

## Disclaimer

This tool is intended for educational purposes only. Always respect Lowes' terms of service and robots.txt file. Use responsibly and ethically.