import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from threading import Thread

class GrabScraper:
    def __init__(self, driver_path, options, proxy=None):
        self.service = Service(executable_path=driver_path)
        self.options = options
        if proxy:
            self.options.add_argument(f'--proxy-server={proxy}')
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def load_all_restaurants(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def scrape_restaurant_data(self, website):
        self.start_driver()
        self.driver.get(website)
        time.sleep(5)  # Wait for the initial page to load

        self.load_all_restaurants()  # Load all restaurants

        restaurants_data = []

        restaurants = self.driver.find_elements(By.CLASS_NAME, 'asList___1ZNTr')

        logging.info(f"Found {len(restaurants)} restaurants.")

        for restaurant in restaurants:
            try:
                name = restaurant.find_element(By.CLASS_NAME, 'name___2epcT').text
                cuisine = restaurant.find_element(By.CLASS_NAME, 'cuisine___T2tCh').text
                rating = restaurant.find_element(By.CLASS_NAME, 'ratingStar').find_element(By.XPATH, '..').text
                delivery_info = restaurant.find_element(By.CLASS_NAME, 'deliveryClock').find_element(By.XPATH, '..').text
                delivery_time, distance = delivery_info.split('•')
                promo_tag = restaurant.find_elements(By.CLASS_NAME, 'promoTagHead___1bjRG')
                promo_available = len(promo_tag) > 0
                promo_text = promo_tag[0].text if promo_available else None
                restaurant_id = restaurant.find_element(By.XPATH, './/img').get_attribute('alt').split(' - ')[0].replace("Order ", "")
                image_link = restaurant.find_element(By.CLASS_NAME, 'realImage___2TyNE').get_attribute('src')

                latitude = None
                longitude = None

                delivery_fee_element = restaurant.find_elements(By.XPATH, '//div[contains(text(), "Delivery fee")]')
                delivery_fee = delivery_fee_element[0].text if delivery_fee_element else None

                restaurant_data = {
                    'Restaurant Name': name,
                    'Restaurant Cuisine': cuisine,
                    'Restaurant Rating': rating,
                    'Estimate time of Delivery': delivery_time.strip(),
                    'Restaurant Distance from Delivery Location': distance.strip(),
                    'Promotional Offers Listed for the Restaurant': promo_text,
                    'Restaurant Notice If Visible': None,
                    'Image Link of the Restaurant': image_link,
                    'Is promo available': promo_available,
                    'Restaurant ID': restaurant_id,
                    'Restaurant Latitude': latitude,
                    'Restaurant Longitude': longitude,
                    'Estimate Delivery Fee': delivery_fee
                }

                logging.info(f"Scraped data for restaurant: {name}")

                restaurants_data.append(restaurant_data)

            except Exception as e:
                logging.error(f"Error occurred: {e}")

        self.stop_driver()
        return restaurants_data

    def scrape(self, website):
        return self.scrape_restaurant_data(website)
