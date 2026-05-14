from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import os
import time

def fetch_html(url):
    """Fetches HTML content of a URL using Playwright.
       This acts like a real browser and helps bypass basic bot protection (like the 403 Forbidden on Goodreads)."""
    print(f"Opening headless browser to fetch: {url}")
    with sync_playwright() as p:
        # Launch Chromium browser in headless mode
        browser = p.chromium.launch(headless=True)
        
        # Create a new context with a realistic User-Agent to look like a normal user
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # Go to the requested URL
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Wait a brief moment to let JavaScript execute and bot checks to finish
            time.sleep(2) 
            
            # Get the fully rendered page HTML content
            html_content = page.content()
            return html_content
        except Exception as e:
            print(f"Error fetching the URL with Playwright: {e}")
            return None
        finally:
            browser.close()

def parse_quotes_toscrape(soup):
    """Parses quotes from quotes.toscrape.com"""
    quotes_data = []
    quote_blocks = soup.find_all('div', class_='quote')
    for block in quote_blocks:
        text = block.find('span', class_='text').get_text(strip=True)
        author = block.find('small', class_='author').get_text(strip=True)
        quotes_data.append({'Quote': text, 'Author': author, 'Source': 'quotes.toscrape.com'})
    return quotes_data

def parse_goodreads_quotes(soup):
    """Parses quotes from goodreads.com/quotes"""
    quotes_data = []
    quote_blocks = soup.find_all('div', class_='quoteDetails')
    for block in quote_blocks:
        quote_text_div = block.find('div', class_='quoteText')
        if not quote_text_div: continue
        
        # Extract the actual quote text cleanly
        full_text = quote_text_div.get_text(separator='|', strip=True).split('|')
        text = full_text[0] if full_text else ""
        
        author = block.find('span', class_='authorOrTitle')
        author_text = author.get_text(strip=True) if author else "Unknown"
        
        # Clean up stray commas in author name from Goodreads formatting
        author_text = author_text.rstrip(',')
        
        quotes_data.append({'Quote': text, 'Author': author_text, 'Source': 'goodreads.com'})
    return quotes_data

def parse_generic_page(soup):
    """Fallback parser that extracts headings and paragraphs for unknown sites."""
    data = []
    headings = soup.find_all(['h1', 'h2', 'h3'])
    for idx, h in enumerate(headings[:15]): # Limit to 15 headings to avoid massive files
        data.append({
            'Content Type': f"Heading ({h.name})",
            'Extracted Text': h.get_text(strip=True),
        })
    return data

def scrape_website(url):
    """Main scraping function that routes to the correct parser based on URL."""
    html_content = fetch_html(url)
    if not html_content:
        return []

    # Parse the dynamically loaded HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Every website has a different HTML structure.
    # We must use specific parsing logic depending on the website we are scraping:
    if "quotes.toscrape.com" in url:
        return parse_quotes_toscrape(soup)
    elif "goodreads.com" in url:
        return parse_goodreads_quotes(soup)
    else:
        print("No specific parser configured for this site. Extracting generic headings...")
        return parse_generic_page(soup)

def save_to_csv(data, filename):
    """Saves the scraped data to a CSV file."""
    if not data:
        print("No data to save.")
        return

    headers = data[0].keys()
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Data successfully saved to: {os.path.abspath(filename)}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__": 
    target_url = "https://www.goodreads.com/quotes"
    # target_url = "https://quotes.toscrape.com/"
    # target_url = "https://www.geeksforgeeks.org/python-programming-language/"
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, "scraped_data.csv")
    
    print(f"Starting scrape of {target_url}...")
    scraped_data = scrape_website(target_url)
    
    if scraped_data:
        print(f"Successfully extracted {len(scraped_data)} records.")
        save_to_csv(scraped_data, output_filename)
    else:
        print("Scraping failed or no data found.")
