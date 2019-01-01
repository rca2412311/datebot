import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# Manual options for the city, num pages to scrape, and URL
pages = 5
cityName = "new-york-city"
websites = [
    'https://pickup-lines.net/',
]

# Load up chrome driver
def init_driver():
    driver = webdriver.Chrome(executable_path="./driver/chromedriver")
    driver.wait = WebDriverWait(driver, 10)
    return driver


def obj_dict(obj):
    return obj.__dict__


def data_export(data):
    print("Appending data")
    with open('./data/pickuplines.txt', "a+") as f:
        for item in data:
            f.write(f"{item} \n")


def parse_HTML(items, data):
    for item in items:
        item = item.contents[0]
        data.append(item)
    return data



def get_data(driver, URL, startPage, endPage, data, refresh):
    if (startPage > endPage):
        return data
    print("\nPage " + str(startPage) + " of " + str(endPage))
    currentURL = URL + "/page/" + str(startPage)
    time.sleep(2)
    if (refresh):
        driver.get(currentURL)
        print("Getting " + currentURL)
    time.sleep(2)
    HTML = driver.page_source
    soup = BeautifulSoup(HTML, "html.parser")
    pickuplines = soup.find("div", { "class" : ["container row clr"] }).find_all("span", { "class" : ["loop-entry-line"] })

    # If there are pick up lines
    if (pickuplines):
        data = parse_HTML(pickuplines, data)
        print("Page " + str(startPage) + " scraped.")
        if (startPage % 10 == 0):
            print("\nTaking a breather for a few seconds ...")
            time.sleep(10)
        data_export(data)
        get_data(driver, URL, startPage + 1, endPage, [], True)
    return data


if __name__ == "__main__":
    driver = init_driver()
    print("\nGet pickup lines ...")
    data = get_data(driver, websites[0], 1, 10000, [], True)
    driver.quit()
