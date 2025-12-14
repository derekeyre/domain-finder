#!/usr/bin/env python3
"""
Company Domain Finder using Google Custom Search API

This script reads company names from a CSV file and uses Google Custom Search API
to find their official domain names.
"""

import csv
import os
import sys
import time
from typing import List, Dict, Optional
import requests


class DomainFinder:
    """Find company domains using Google Custom Search API."""

    def __init__(self, api_key: str, cx_id: str):
        """
        Initialize the DomainFinder.

        Args:
            api_key: Google API key
            cx_id: Google Custom Search Engine ID
        """
        self.api_key = api_key
        self.cx_id = cx_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search_company_domain(self, company_name: str) -> Optional[Dict[str, str]]:
        """
        Search for a company's domain using Google Custom Search API.

        Args:
            company_name: Name of the company to search for

        Returns:
            Dictionary with company name, domain, and URL, or None if not found
        """
        try:
            # Build the search query
            query = f"{company_name} official website"

            params = {
                'key': self.api_key,
                'cx': self.cx_id,
                'q': query,
                'num': 1  # Only get the top result
            }

            # Make the API request
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            data = response.json()

            # Extract domain from the first search result
            if 'items' in data and len(data['items']) > 0:
                first_result = data['items'][0]
                url = first_result.get('link', '')

                # Extract domain from URL
                domain = self._extract_domain(url)

                return {
                    'company': company_name,
                    'domain': domain,
                    'url': url,
                    'title': first_result.get('title', '')
                }
            else:
                print(f"No results found for: {company_name}")
                return {
                    'company': company_name,
                    'domain': 'NOT_FOUND',
                    'url': '',
                    'title': ''
                }

        except requests.exceptions.RequestException as e:
            print(f"Error searching for {company_name}: {e}")
            return {
                'company': company_name,
                'domain': 'ERROR',
                'url': '',
                'title': str(e)
            }

    @staticmethod
    def _extract_domain(url: str) -> str:
        """
        Extract domain from a URL.

        Args:
            url: Full URL

        Returns:
            Domain name
        """
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc
            # Remove 'www.' prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except Exception:
            return url

    def process_csv(self, input_file: str, output_file: str, delay: float = 1.0):
        """
        Process a CSV file of company names and find their domains.

        Args:
            input_file: Path to input CSV file with company names
            output_file: Path to output CSV file for results
            delay: Delay in seconds between API requests to avoid rate limits
        """
        results = []

        # Read company names from CSV
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Support both 'company' and 'company_name' column headers
                companies = []
                for row in reader:
                    if 'company' in row:
                        companies.append(row['company'])
                    elif 'company_name' in row:
                        companies.append(row['company_name'])
                    elif 'name' in row:
                        companies.append(row['name'])
                    else:
                        # If no recognized header, use first column
                        companies.append(list(row.values())[0])
        except FileNotFoundError:
            print(f"Error: Input file '{input_file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)

        # Process each company
        total = len(companies)
        print(f"Processing {total} companies...")

        for idx, company in enumerate(companies, 1):
            if not company or not company.strip():
                continue

            print(f"[{idx}/{total}] Searching for: {company}")
            result = self.search_company_domain(company.strip())

            if result:
                results.append(result)
                print(f"  → Found: {result['domain']}")

            # Add delay to avoid rate limiting (except for last item)
            if idx < total:
                time.sleep(delay)

        # Write results to output CSV
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['company', 'domain', 'url', 'title']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)

            print(f"\nResults saved to: {output_file}")
            print(f"Total companies processed: {len(results)}")

        except Exception as e:
            print(f"Error writing output file: {e}")
            sys.exit(1)


def main():
    """Main function."""
    # Get API credentials from environment variables
    api_key = os.getenv('GOOGLE_API_KEY')
    cx_id = os.getenv('GOOGLE_CX_ID')

    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set")
        sys.exit(1)

    if not cx_id:
        print("Error: GOOGLE_CX_ID environment variable not set")
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python find_domains.py <input_csv> [output_csv] [delay_seconds]")
        print("\nExample: python find_domains.py companies.csv results.csv 1.0")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'results.csv'
    delay = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    # Create finder and process CSV
    finder = DomainFinder(api_key, cx_id)
    finder.process_csv(input_file, output_file, delay)


if __name__ == '__main__':
    main()
