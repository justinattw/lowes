#!/usr/bin/env python3
import json
import time
import random
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import requests
from bs4 import BeautifulSoup
import logging
# Import the functions from utils
from utils import load_pages_from_json, save_results_to_json

@dataclass
class Page:
    name: str
    url: str
    categories: List["Page"] = None
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = []
    
    def is_scrapable(self) -> bool:
        """A page is considered final if it has no categories. 
        This means it can be scraped for products."""
        return len(self.categories) == 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Page":
        """Create a Page object from a dictionary."""
        categories = []
        if "categories" in data and data["categories"]:
            categories = [Page.from_dict(cat) for cat in data["categories"]]
        
        return cls(
            name=data["name"],
            url=data["url"],
            categories=categories
        )

class LowesScraperConfig:
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    ]
    
    DELAY_MIN = 2  # Minimum delay in seconds between requests
    DELAY_MAX = 5  # Maximum delay in seconds between requests
    
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

class LowesScraper:
    def __init__(self, config: LowesScraperConfig = None):
        self.config = config or LowesScraperConfig()
        self.session = requests.Session()
        self.results = []
    
    def _get_random_user_agent(self) -> str:
        """Get a random user agent from the predefined list."""
        return random.choice(self.config.USER_AGENTS)
    
    def _add_delay(self):
        """Add a random delay between requests to avoid rate limiting."""
        delay = random.uniform(self.config.DELAY_MIN, self.config.DELAY_MAX)
        self.config.logger.debug(f"Sleeping for {delay:.2f} seconds")
        time.sleep(delay)

    def scrape(self, page: Page) -> Dict[str, Any]:
        """Scrape data from a page and return the results."""
        if page.is_scrapable():
            self.scrape_page(page)
        else:
            for subpage in page.categories:
                self.config.logger.info(f"Entering subpage with category: {subpage.name}")
                self.scrape(subpage)

        return results
    
    def scrape_page(self, page: Page) -> Dict[str, Any]:
        """Scrape data from a single page."""
        self.config.logger.info(f"Scraping page: {page.name} - {page.url}")
        
        headers = {
            'User-Agent': self._get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.lowes.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        try:
            response = self.session.get(page.url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data - this is a basic example, adjust according to what you need
            product_items = soup.select('div.tile-group__item')
            products = []
            
            for item in product_items:
                product = {}
                
                # Extract product title
                title_element = item.select_one('.tile-title')
                if title_element:
                    product['title'] = title_element.text.strip()
                
                # Extract price
                price_element = item.select_one('.tile-price__dollars')
                if price_element:
                    product['price'] = price_element.text.strip()
                
                # Extract product image
                img_element = item.select_one('img.product-image')
                if img_element and img_element.has_attr('src'):
                    product['image'] = img_element['src']
                
                # Extract product URL
                link_element = item.select_one('a.tile')
                if link_element and link_element.has_attr('href'):
                    product['url'] = 'https://www.lowes.com' + link_element['href'] if link_element['href'].startswith('/') else link_element['href']
                
                if product:
                    products.append(product)
            
            result = {
                'name': page.name,
                'url': page.url,
                'products': products,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
        
        except Exception as e:
            self.config.logger.error(f"Error scraping {page.url}: {str(e)}")
            return {
                'name': page.name,
                'url': page.url,
                'error': str(e),
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        finally:
            self._add_delay()
    
    def find_all_final_pages(self, root_page: Page) -> List[Page]:
        """Find all final pages (those with empty categories) recursively."""
        final_pages = []
        
        if root_page.is_final_page():
            final_pages.append(root_page)
        else:
            for category in root_page.categories:
                final_pages.extend(self.find_all_final_pages(category))
        
        return final_pages
    
    def scrape_all_final_pages(self, root_page: Page) -> Dict[str, Any]:
        """Scrape all final pages and return the results."""
        final_pages = self.find_all_final_pages(root_page)
        self.config.logger.info(f"Found {len(final_pages)} final pages to scrape")
        
        results = []
        for page in final_pages:
            result = self.scrape_page(page)
            results.append(result)
        
        return {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_pages': len(final_pages),
            'results': results
        }

# Functions moved to utils.py


