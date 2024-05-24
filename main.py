import logging
from selenium import webdriver
from scraper.grab_scraper import GrabScraper
from scraper.data_processor import DataProcessor
from threading import Thread
from environment import driver_path, proxy

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
    
    website = "https://food.grab.com/sg/en/restaurants"
    output_file = 'restaurants.ndjson'

    scraper = GrabScraper(driver_path, options, proxy)
    
    def scrape_data():
        data = scraper.scrape(website)
        unique_data = DataProcessor.unique_restaurants(data)
        DataProcessor.save_to_ndjson(unique_data, output_file)
        logging.info(f"Data saved to {output_file}")

    scrape_thread = Thread(target=scrape_data)
    scrape_thread.start()
    scrape_thread.join()

if __name__ == "__main__":
    main()
