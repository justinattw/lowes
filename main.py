import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("lowes_scraper")

def main():
    # Load the pages structure from the JSON file
    json_file_path = "pages.json"
    output_file_path = "results.json"
    
    logger.info(f"Loading pages from {json_file_path}")
    root_page = load_pages_from_json(json_file_path)
    
    # Initialize the scraper
    scraper = LowesScraper()
    
    # Scrape all final pages
    logger.info("Starting to scrape final pages")
    results = scraper.scrape_all_final_pages(root_page)
    
    # Save the results
    logger.info(f"Saving results to {output_file_path}")
    save_results_to_json(results, output_file_path)
    
    logger.info(f"Scraping completed. Scraped {results['total_pages']} pages.")

if __name__ == "__main__":
    main()