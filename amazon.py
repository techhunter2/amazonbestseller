import csv
import re
import time
from datetime import date
from time import strftime

import pandas as pd
import requests
import schedule
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import config
import scroll

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}
AMAZON_URL = "https://www.amazon.sg/gp/bestsellers"


def get_first_text(node, xpath, default=""):
    try:
        matches = node.xpath(xpath)
        if matches:
            text = matches[0].text_content().strip()
            if text:
                return text
    except Exception:
        pass
    return default


def extract_asin(url):
    match = re.search(r"/[dg]p/([^/?]+)", url, flags=re.IGNORECASE)
    return match.group(1) if match else ""


def extract_category_slug(category_url):
    match = re.search(r"/bestsellers/([^/?]+)", category_url, flags=re.IGNORECASE)
    return match.group(1) if match else ""


def fetch_product_page(url):
    for _ in range(3):
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            if response.status_code == 200:
                return html.fromstring(response.content)
        except Exception:
            time.sleep(1)
    return None


def extract_product_data(url, category_url):
    tree = fetch_product_page(url)
    if tree is None:
        return None

    product = {
        "Date": str(date.today()),
        "Title": get_first_text(tree, "//span[@id='productTitle']"),
        "Price": get_first_text(tree, "//div[contains(@class,'a-section') and contains(@class,'a-spacing-none') and contains(@class,'aok-align-center')]//span//span"),
        "No of Rating": get_first_text(tree, "//span[@id='acrCustomerReviewText']"),
        "Manufacturer": get_first_text(tree, "//th[contains(normalize-space(.), 'Manufacturer')]/following-sibling::td[1]"),
        "ASIN": extract_asin(url),
        "Categories": extract_category_slug(category_url),
        "Rank": "",
        "Best_Seller_In": get_first_text(tree, "//span[contains(@class,'cat-link')]"),
        "Sold By": get_first_text(tree, "//div[@id='merchant-info']//a//span"),
        "Full_filled_by": get_first_text(tree, "//div[@id='merchant-info']//span"),
        "Rating": get_first_text(tree, "//i[contains(@class,'a-icon-star')]/span"),
        "International Ratings": get_first_text(tree, "//div[contains(@class,'review') and contains(@class,'a-color-alternate-background')]//div"),
        "Global Rating": get_first_text(tree, "//div[@data-hook='total-review-count']//span"),
        "Url": url,
    }
    return product


def amazon_scraping():
    print("Scrapping is started at daily " + config.schd_time)
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(20)
    driver.maximize_window()

    all_data = []
    print("----------- Scrapping Started -----------")

    try:
        driver.get(AMAZON_URL)
        category_links = [
            link.get_attribute("href")
            for link in driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'zg-browse-group') or contains(@class,'_p13n-zg-nav-tree-all_style_zg-browse-group__88fbz')]//a[@href]"
            )
        ]

        for category_url in category_links:
            if not category_url:
                continue
            driver.get(category_url)
            time.sleep(1)
            try:
                scroll.scroll(driver, 2)
            except Exception:
                pass

            product_links = [
                link.get_attribute("href")
                for link in driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class,'zg-grid-general-faceout')]//a[contains(@href,'/dp/') or contains(@href,'/gp/product/') or contains(@href,'/product/')]"
                )
            ]

            seen = set()
            for rank, product_url in enumerate(product_links, start=1):
                if not product_url or product_url in seen:
                    continue
                seen.add(product_url)

                record = extract_product_data(product_url, category_url)
                if record is None:
                    continue
                record["Rank"] = rank
                all_data.append(record)
    finally:
        driver.quit()

    if all_data:
        df = pd.DataFrame(all_data)
        curr_time = strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        df.to_csv(f"{curr_time}-amazon_scraped.csv", index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
        print(f"Scrapping is done next scrapping will begin at {config.schd_time}")
    else:
        print("No data was scraped.")


if __name__ == "__main__":
    print("Scrapping will start at daily " + config.schd_time)
    schedule.every().day.at(config.schd_time).do(amazon_scraping)
    while True:
        schedule.run_pending()
        time.sleep(1)
