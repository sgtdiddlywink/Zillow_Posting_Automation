"""
This script will follow the link to zillow below that already has the custom search.  This can be modified.
BeautifulSoup will then scrape the web page for all listings, create lists for the link, price, and address of the
first 9 postings.  These will then be added to a custom google form that you can use to create a spreadsheet of the
listings.

This script unfortunately only grabs the first 9 postings on the search page.  Future script will fully utilize
Selenium to scroll through each listing and grab the information.

Note: You will need to update your header information from the link: http://myhttpheader.com/.
"""
"""Import and install appropriate modules below."""
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Link to the Zillow search.  This can be modified depending on your preference.
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A42." \
             "44619635745188%2C%22east%22%3A-70.75648730468751%2C%22south%22%3A42.26987642788133%2C%22west%22%3" \
             "A-71.37790148925782%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22m" \
             "ax%22%3A896455%7D%2C%22beds%22%3A%7B%22min%22%3A2%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%" \
             "22mp%22%3A%7B%22max%22%3A4500%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value" \
             "%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%" \
             "22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22baths%22%3A%7" \
             "B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22pagination%22%3A%7B%7D%7D"

# Link to your Google form which will auto populate a spreadsheet with the information.  Create your own Google Form
# with the information you want to collect.  This script only collects address, price, and link to posting.
GOOGLE_FORM_LINK = "CREATE YOUR OWN GOOGLE FORM WITH THREE SHORT QUESTIONS.  WHAT IS THE ADDRESS, LINK, AND PRICE."

# Zillow will require headers to utilize Beautiful Soup.  Use: http://myhttpheader.com/ to obtain your headers.
# These will most likely change for each person and you will need to update them.
headers = {"PLACE YOUR OWN HEADERS HERE"}

# Perform a get request to obtain information from Zillow website.
data = requests.get(
    url=ZILLOW_URL,
    headers=headers,
)

# Perform a status update to confirm you are able to access the website.
data.raise_for_status()

# Create a soup object from the get request previously.
soup = BeautifulSoup(data.text, features="lxml")

# Obtain information from side panel list of all postings to search.
grid_list = soup.find_all(name="ul")[5]

# Obtain links to each posting and create a list out of them.
link = [n.get("href") for n in grid_list.find_all(name="a", class_="StyledPropertyCardDataArea-c11n-8-69-2__sc-yipmu-0")]
print(link)
hyperlink_list = []
for n in link:
    if "https://www.zillow.com" not in n:
        hyperlink_list.append("https://www.zillow.com" + n)
    else:
        hyperlink_list.append(n)
print(hyperlink_list)

# Obtain prices from each posting.
price = [n.get_text() for n in grid_list.find_all(name="span", attrs={"data-test": "property-card-price"})]
price_list = []
for n in price:
    if n != "" and n != "Three Dimensional 3D Tour":
        price_list.append(n)
print(price_list)

# Obtain addresses from each listing.
addresses = [n.get_text() for n in grid_list.find_all(name="address", attrs={"data-test": "property-card-addr"})]
addresses_list = [n.split("|")[-1] for n in addresses]
print(addresses_list)

"""Need to install the appropriate browser driver and place .exe in accessible file."""
# Chrome driver path should reference the .exe browser driver.
chrome_driver_path = "PUT THE FILE PATH TO YOUR DRIVER."

# Create object from selenium class.
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# # Utilize selenium object to open a website.
# driver.get(url=GOOGLE_FORM_LINK)

# # Sleep for 2 seconds to let page submit and load next one.
# time.sleep(2)

# For loop to run through each item in the lists and input them into the form.
for n in range(len(addresses_list)):
    # Sleep for 3 seconds to let page submit and load next one.
    time.sleep(2)
    # Utilize selenium object to open a website.
    driver.get(url=GOOGLE_FORM_LINK)
    # Sleep for 3 seconds to let page submit and load next one.
    time.sleep(2)
    # Add the address to the form.
    driver.find_element(
        By.XPATH,
        "//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input"
    ).send_keys(addresses_list[n])
    # Add the price to the form.
    driver.find_element(
        By.XPATH,
        "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input"
    ).send_keys(price_list[n])
    # Add the hyperlink to the form.
    driver.find_element(
        By.XPATH,
        "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input"
    ).send_keys(hyperlink_list[n])
    # Click the submit button.
    driver.find_element(
        By.XPATH,
        "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span"
    ).click()



