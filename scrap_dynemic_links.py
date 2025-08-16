from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json

def scrape_all_links(property_type, bhk, city, scroll_count):
    url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom={bhk}&proptype={property_type}&cityName={city}"
    print("Scraping links from:", url)
    service = Service('chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.binary_location = r"C:/Users/moham/OneDrive/Desktop/chrome-win64/chrome-win64/chrome.exe"
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(4)

    for i in range(scroll_count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Scrolled {i+1} times...")
        time.sleep(4)

    # Get full page source
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, "html.parser")
    script_tags = soup.find_all("script", {"type": "application/ld+json"})

    property_links = set()

    for script in script_tags:
        try:
            content = script.string
            if not content:
                continue
            data = json.loads(content)

            # Case 1: Single listing
            if isinstance(data, dict) and data.get("@type") in ["Apartment", "SingleFamilyResidence", "Land"]:
                link = data.get("url")
                if link and "magicbricks.com/propertyDetails/" in link:
                    property_links.add(link)

            # Case 2: List of items
            elif isinstance(data, dict) and data.get("@type") == "ItemList":
                for item in data.get("itemListElement", []):
                    link = item.get("url")
                    if link and "magicbricks.com/propertyDetails/" in link:
                        property_links.add(link)

        except Exception as e:
            continue

    return list(property_links)

links = scrape_all_links(  "Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa" , "2,3,4" , "Ahmedabad", 5)

print( 'total ',len(links), ' links found')
for link in links:
    with open("links.txt", "a") as file:
        file.write(link + "\n")