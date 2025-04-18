#!/usr/bin/env python3
import json
from typing import Dict, Any

from scraper import Page

def load_pages_from_json(json_file_path: str) -> Page:
    """Load the pages structure from a JSON file."""
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    return Page.from_dict(data)

def save_results_to_json(results: Dict[str, Any], output_file_path: str):
    """Save the scraping results to a JSON file."""
    with open(output_file_path, 'w') as f:
        json.dump(results, f, indent=2)
