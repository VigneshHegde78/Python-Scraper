# Python Web Scraper

A robust, modern Python web scraper that leverages **Playwright** and **BeautifulSoup** to extract data from websites. 

Unlike basic scrapers using `requests`, this script uses a headless Chromium browser to execute JavaScript and dynamically load content. This allows it to easily bypass basic bot-protection mechanisms (like 403 Forbidden errors) found on modern websites such as Goodreads.

## Features

- **Headless Browser Automation**: Uses Playwright to mimic real human browsing behavior.
- **Dynamic Content Support**: Fully renders JavaScript-heavy websites before parsing.
- **Modular Parsers**: Contains distinct parsing logic for different websites (e.g., `quotes.toscrape.com`, `goodreads.com`).
- **CSV Export**: Automatically cleans extracted data and exports it to a nicely formatted `.csv` file.

## Prerequisites

Before running the script, ensure you have Python installed. You will also need to install the required libraries and the Playwright browser binaries.

## Installation

1. Clone this repository (or download the script).
2. Install the required Python dependencies:
   ```bash
   pip install playwright beautifulsoup4
   ```
3. Install the Playwright Chromium browser binaries:
   ```bash
   playwright install chromium
   ```

## Usage

1. Open `web_scraper.py` in your code editor.
2. Scroll to the bottom of the script to the `if __name__ == "__main__":` block.
3. Set the `target_url` variable to the website you want to scrape.
   ```python
   target_url = "https://www.goodreads.com/quotes"
   ```
4. Run the script:
   ```bash
   python web_scraper.py
   ```
5. The extracted data will be saved in a file named `scraped_data.csv` in the same directory.

## Customization (Adding New Sites)

Web scraping is heavily dependent on a website's specific HTML structure. If you want to scrape a new website:
1. Inspect the website's HTML to find the classes or IDs of the data you want.
2. Create a new parsing function in the script (similar to `parse_goodreads_quotes`).
3. Update the routing logic in the `scrape_website(url)` function to call your new parser when it detects the target URL.
