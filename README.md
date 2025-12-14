# Company Domain Finder

A Python script that uses Google Custom Search API to find company domains from a CSV file of company names.

## Features

- Reads company names from a CSV file
- Uses Google Custom Search API to find official company websites
- Extracts domain names from search results
- Outputs results to a CSV file with domain, URL, and page title
- Includes rate limiting to avoid API quota issues
- Error handling for API failures and missing data

## Prerequisites

1. **Google API Key**: You need a Google API key with Custom Search API enabled
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project or select an existing one
   - Enable the Custom Search API
   - Create credentials (API key)

2. **Custom Search Engine ID**: You need to create a Custom Search Engine
   - Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
   - Create a new search engine
   - Set it to search the entire web
   - Copy the Search Engine ID (cx)

## Setup

1. Clone this repository:
```bash
git clone https://github.com/derekeyre/domain-finder.git
cd domain-finder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables with your credentials:
```bash
export GOOGLE_API_KEY="your_api_key_here"
export GOOGLE_CX_ID="your_search_engine_id_here"
```

## Usage

### Basic Usage

```bash
python find_domains.py companies.csv
```

This will read from `companies.csv` and output results to `results.csv` (default).

### Specify Output File

```bash
python find_domains.py companies.csv output.csv
```

### Customize API Request Delay

To avoid rate limiting, you can set a delay (in seconds) between API requests:

```bash
python find_domains.py companies.csv output.csv 2.0
```

This sets a 2-second delay between requests.

## Input CSV Format

The input CSV should have a column with company names. The script supports these column headers:
- `company`
- `company_name`
- `name`

If none of these headers are present, it will use the first column.

### Example Input CSV

```csv
company
Microsoft
Apple
Google
Amazon
```

## Output CSV Format

The output CSV will contain:
- `company`: Original company name
- `domain`: Extracted domain name
- `url`: Full URL of the top search result
- `title`: Page title from search result

### Example Output CSV

```csv
company,domain,url,title
Microsoft,microsoft.com,https://www.microsoft.com/,Microsoft - Official Home Page
Apple,apple.com,https://www.apple.com/,Apple
Google,google.com,https://www.google.com/,Google
Amazon,amazon.com,https://www.amazon.com/,Amazon.com: Online Shopping
```

## API Limits

Google Custom Search API free tier includes:
- 100 queries per day
- For more queries, you'll need to enable billing

The script includes a 1-second delay between requests by default to help manage rate limits.

## Error Handling

- If a company domain is not found, the domain field will show `NOT_FOUND`
- If there's an API error, the domain field will show `ERROR` and the title will contain the error message

## License

MIT License - Feel free to use and modify as needed.
