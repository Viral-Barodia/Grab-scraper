# Grab-scraper

### Made this scraper to get information about restaurants in a particular localoty of Singapore. I used the Grab website to scrape the data of all the restaurants. It automatically scrolls to the bottom of the window of the home page, since the data of the website loads content dynamically when the user scrolls further down.

### In order to run the scraper:
1. Clone the repo in your local machine
2. Install the driver for your web-browser, and put it's link in the driver_path variable in the environment file
3. If you have a proxy that you'd like the scraper to use, put it with the port number in the proxy variable in the environment file
4. And then, simply run the following command: `python main.py`

### This will run the scraper and put the result in the restaurants.ndjson
