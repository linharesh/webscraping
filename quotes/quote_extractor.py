import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

OUTPUT_FILE_NAME = "quotes.jsonl"
HEADLESS = True


def create_webdriver(browser="FIREFOX"):
    print("Starting webdriver")
    if browser.upper() == "FIREFOX":
        try:
            options = webdriver.FirefoxOptions()
            if HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Firefox(options=options)
            return driver
        except Exception as e:
            print("Could not start webdriver. Error: " + str(e))
    else:
        raise ValueError(f"Browser '{browser}' is not supported yet")


def append_to_jsonl(file_path, data):
    with open(file_path, "a", encoding="utf8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def extract_quotes_current_page(driver, output_file):
    quotes = driver.find_elements(By.CSS_SELECTOR, ".quote")
    extracted_quote_count = 0
    for quote in quotes:
        try:
            quote_data = None
            text = quote.find_element(By.CSS_SELECTOR, ".text").text
            author = quote.find_element(By.CSS_SELECTOR, ".author").text
            tags = [tag.text for tag in quote.find_elements(By.CSS_SELECTOR, ".tag")]
            quote_data = {"text": text, "author": author, "tags": tags}
        except Exception as e:
            print(e)
        if quote_data:
            extracted_quote_count += 1
            append_to_jsonl(output_file, quote_data)
    print(
        f"Extracted {str(extracted_quote_count)} quotes from page {driver.current_url}"
    )
    return extracted_quote_count


def main_extract_quotes(output_file):
    total_quotes_count = 0
    start_time = datetime.now()
    driver = create_webdriver()
    try:
        has_next = True
        driver.get("http://quotes.toscrape.com/js/")
        while has_next:
            time.sleep(1.5)
            print("Current page is: " + driver.current_url)
            count = extract_quotes_current_page(driver, output_file)
            total_quotes_count += count
            next_button = driver.find_elements(By.CSS_SELECTOR, ".next a")
            if next_button:
                next_button[0].click()
                print("Navigate to next page")
                print()
            else:
                has_next = False
    finally:
        print("Finishing webdriver")
        driver.quit()
    end_time = datetime.now()
    duration = end_time - start_time
    print(
        f"Extracted a total of {total_quotes_count} quotes in {duration.seconds // 60} minutes and {duration.seconds % 60} seconds"
    )
    print(f"Output file is : {output_file}")


if __name__ == "__main__":
    main_extract_quotes(OUTPUT_FILE_NAME)
