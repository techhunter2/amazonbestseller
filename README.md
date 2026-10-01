# Amazon Trending Items Scraper

This project scrapes Amazon best-selling and trending products from different categories and stores the extracted details into a CSV file.

It is designed to collect product information across category pages on Amazon Singapore (`amazon.sg`), including:

- product title
- price
- rating
- review count
- manufacturer
- ASIN
- category
- rank
- seller information
- product URL
- date of scraping

## Project purpose

The script visits Amazon's best-seller pages, finds category links, opens each category, collects product links, and extracts product details from each listing. The output is saved in a timestamped CSV file such as:

`YYYY-MM-DD HH-MM-SS-amazon_scraped.csv`

## Folder contents

- `amazon.py` - main scraping logic
- `config.py` - scheduler configuration
- `scroll.py` - helper for page scrolling
- `requirments.txt` - Python dependencies
- CSV files - generated scraped output files

## Requirements

This project uses Python and requires the following packages:

- selenium
- requests
- pandas
- lxml
- schedule

You can install them with:

```bash
pip install -r requirments.txt
```

## Setup

1. Open the project folder.
2. Make sure Chrome is installed on your machine.
3. Install the Python dependencies.
4. Ensure the ChromeDriver is available for Selenium.
5. Update the schedule time in `config.py` if needed.

Example:

```python
schd_time = '13:12'
```

This means the scraper is scheduled to run daily at 13:12.

## Run the scraper

From the project folder, run:

```bash
python amazon.py
```

The script will:

- open the Amazon best-sellers page
- collect category links
- scrape product listings from each category
- save the results to a CSV file
- repeat daily at the configured schedule time

## Output format

Each row in the CSV contains fields such as:

- Date
- Title
- Price
- No of Rating
- Manufacturer
- ASIN
- Categories
- Rank
- Best_Seller_In
- Sold By
- Full_filled_by
- Rating
- International Ratings
- Global Rating
- Url

## Important notes

- This scraper depends on Amazon's current HTML structure, which may change over time.
- XPath selectors may need updates if Amazon modifies their page layout.
- It is intended for learning and data collection purposes.
- Please respect Amazon's terms of service and robots policies when using this project.

## Disclaimer

This project is for educational and personal data collection use. Always check the relevant platform terms before scraping websites or automating browser activity.
