from bs4 import BeautifulSoup
import json
import requests
import re
import traceback
# property_id : <span class="mb-ldp__posted--propid">Property ID: 80819655</span>
# price : <div class="mb-ldp__dtls__price"><span class="rupees">₹</span>1.55 Cr </div>
# bhk : from url (no need to scrape)
# total_area : from url (no need to scrape)
# carpet_area : <div class="mb-ldp__dtls__body__list">1346<span class="mb-ldp__dtls__body__list--units"><span>sqft</span><ul id="unitsList" class="mb-ldp__dtls__body__list--drop-down"><li>sqft</li><li>sqyrd</li><li>sqm</li><li>acre</li><li>bigha</li><li>hectare</li><li>marla</li><li>kanal</li><li>biswa1</li><li>biswa2</li><li>ground</li><li>aankadam</li><li>rood</li><li>chatak</li><li>kottah</li><li>marla</li><li>cent</li><li>perch</li><li>guntha</li><li>are</li><li>katha</li><li>gaj</li><li>killa</li><li>kuncham</li></ul></span></div>
# furnishing : <div class="mb-ldp__dtls__body__list--value">Unfurnished</div>
# status : <div class="mb-ldp__dtls__body__list--value">Under Construction</div>
# other_details : <script type="application/ld+json">
#         {
#             "@context": "http://schema.org/",                
#              "type": "Apartment",
#             "name": "3 BHK Multistorey Apartment  2520 ",
#             "description": "3 Bath, , Unfurnished",
#             "url": "https://www.magicbricks.com/propertyDetails/3-BHK-2520-Sq-ft-Multistorey-Apartment-FOR-Sale-Gota-in-Ahmedabad&id=4d423737323832383437", 
#                 "numberOfRooms": "3",  
#             "address": {
#                 "@type": "PostalAddress",    
#                     "addressLocality": "Gota",
#                     "addressRegion": "Ahmedabad",
#                 "addressCountry": {
#                     "@type": "Country",     
#                     "name": "IN"
#                 }
#             }
#              ,
#                 "geo": {
#                     "@type": "GeoCoordinates",
#                     "longitude": "72.53525427868169",
#                     "latitude": "23.08511854314398"
#                 }	
#              ,
#                 "floorSize": {
#                     "@type": "QuantitativeValue",
#                     "name": "2520 FTK"
#                 }		
#         }
# </script>
def fetch_locality_ratings(locality_id):
    url = f"https://www.magicbricks.com/mbldp/localityDetailInfo?localityId={locality_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            ratings = {
                "connectivity": data.get("connectivityRating"),
                "safety": data.get("safetyRating"),
                "traffic": data.get("trafficRating"),
                "environment": data.get("environmentRating"),
                "market": data.get("marketRating"),
                "area_description": data.get("areaDescription", "")
            }
            return ratings
        else:
            print("Locality rating API returned non-200 status:", response.status_code)
    except Exception as e:
        print("Error fetching locality ratings:", e)

    return {}
def fetch_gallery_photos(prop_id):
    url = f"https://www.magicbricks.com/photoapi/property/photos?propId={prop_id}&type=large"
    headers = {"User-Agent": "Mozilla/5.0"}
    prop_photos = []
    project_photos = []
    locality_photos = []
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # Property Photos
        if "propPhotos" in data:
            for category in data["propPhotos"]:
                for photo in category.get("photos", []):
                    if "url" in photo:
                        prop_photos.append(photo["url"])
        # Project Photos
        if "projectPhotos" in data:
            for category in data["projectPhotos"]:
                for photo in category.get("photos", []):
                    if "url" in photo:
                        project_photos.append(photo["url"])
        # Locality Photos
        if "localityPhotos" in data:
            for category in data["localityPhotos"]:
                for photo in category.get("photos", []):
                    if "url" in photo:
                        locality_photos.append(photo["url"])
    except Exception as e:
        print(f"Failed to fetch gallery photos for {prop_id}: {e}")
    return prop_photos, project_photos, locality_photos


import requests
import json

def fetch_investment_data(psmid, property_type_code, locality_id, locality_name):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url = (
        "https://www.magicbricks.com/mbldp/Project-Rates-Trends-Month?"
        f"&psmid={psmid}&propType={property_type_code}&localityid={locality_id}&localityName={locality_name}"
    )

    property_yield = None
    months = []
    prices = []

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                print("Response is not valid JSON:")
                print(response.text[:500])  # print first 500 characters for inspection
                return {}
            
            # Extract property yield if available
            nearby = data.get("currentPricesNearbyMap", [])
            for item in nearby:
                if item.get("loc") == "Locality Average":
                    property_yield = item.get("Yield")

            # Proceed only if JSON decoding was successful
            months_str = data.get("monthYrAvgPriceStr", "")
            months = [m.strip().strip('"') for m in months_str.split(",")]

            locality_key = str(locality_id)
            locality_raw = data.get("localitiesDataMap", {}).get(locality_key)
            if locality_raw:
                locality_data = json.loads(locality_raw).get("data", [])
                prices = []
                for entry in locality_data:
                    if isinstance(entry, dict) and "y" in entry:
                        prices.append(entry["y"])
                    elif isinstance(entry, (int, float)):
                        prices.append(entry)
                    else:
                        prices.append(None)
            else:
                print("No locality data found for", locality_key)
        else:
            print("Request failed. Status code:", response.status_code)

    except Exception as e:
        print("Unexpected error occurred:", e)

    
    historical_price = {month: price for month, price in zip(months, prices)}
    property_yield = property_yield if property_yield is not None else "N/A"
    return historical_price, property_yield



def scrape_property_details(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    scripts = soup.find_all("script", type="application/ld+json")
    property_data = {}

    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") != "Organization":
                property_data = data
                break
        except:
            continue
    name = property_data.get("name", "").strip()    
    property_type = property_data.get("type", "").strip()
    description = property_data.get("description", "").strip()
    rooms = property_data.get("numberOfRooms", "")
    floor_size = property_data.get("floorSize", {}).get("name", "")
    latitude = property_data.get("geo", {}).get("latitude")
    longitude = property_data.get("geo", {}).get("longitude")
    locality = property_data.get("address", {}).get("addressLocality", "")
    region = property_data.get("address", {}).get("addressRegion", "")

    # Extract property ID from the tag
    property_id = soup.find("span", class_="mb-ldp__posted--propid")
    if property_id:
        property_id = property_id.get_text(strip=True).split(":")[-1].strip()
    else:
        property_id = None

    price = soup.find("div", class_="mb-ldp__dtls__price")
    price = price.get_text(strip=True) if price else None
    bhk = url.split("/")[4].split("-")[0] if len(url.split("/")) > 4 else None
    total_area = url.split("/")[4].split("-")[2] if len(url.split("/")) > 4 else None
    
    property_photos,project_photos,locality_photos = fetch_gallery_photos(property_id) if property_id else ([], [])

    details = {}
    list_items = soup.select("ul.mb-ldp__dtls__body__list > li.mb-ldp__dtls__body__list--item")
    for item in list_items:
        label_tag = item.select_one(".mb-ldp__dtls__body__list--label")
        value_tag = item.select_one(".mb-ldp__dtls__body__list--value")

        if not label_tag or not value_tag:
            continue

        label = label_tag.get_text(strip=True)

        # Special case for Carpet Area + Price per sqft
        if label == "Carpet Area":
            size_tag = value_tag.select_one(".mb-ldp__dtls__body__list")
            ppsf_tag = value_tag.select_one(".mb-ldp__dtls__body__list--size")
            size = size_tag.get_text(strip=True) if size_tag else None
            ppsf = ppsf_tag.get_text(strip=True) if ppsf_tag else None
            details["Carpet Area"] = size
            details["Price Per Sqft"] = ppsf
        else:
            value = value_tag.get_text(strip=True)
            details[label] = value

    # extract historical data from this api : https://www.magicbricks.com/mbldp/Project-Rates-Trends-Month?&psmid=<psmid>&propType=<propertyTypeCode>&localityid=<localityId>&localityName=<localityName>
    # psmid : in url of project union property photoes : https://img.staticmb.com/mbimages/project/Photo_h470_w1080/2025/01/23/Project-Photo-11-Unique-Luxuria-Ahmedabad-5418089_410_1440_470_1080.jpg"
    # "5418089" is psmid extract it using regex
    psmid = None
    all_photos = (project_photos or []) + (property_photos or [])

    for url in all_photos:
        match = re.search(r'-([0-9]{6,})_[0-9]+(?:_[0-9]+)*\.jpg$', url)
        if match:
            psmid = match.group(1)
            break


    target_script = None
    for script in soup.find_all("script"):
        if script.string and "window.SERVER_PRELOADED_STATE_DETAILS" in script.string:
            target_script = script.string
            break
    match = re.search(r'window\.SERVER_PRELOADED_STATE_DETAILS\s*=\s*({.*});', target_script, re.DOTALL)
    if match:
        json_text = match.group(1)
        try:
            data = json.loads(json_text)
            property_type_code = (
                data.get("propertyDetailInfoBeanData", {})
                    .get("propertyDetail", {})
                    .get("detailBean", {})
                    .get("propertyTypeCode")
            )
            locality_id = data.get("propertyDetailInfoBeanData", {}).get("localityId")
        except json.JSONDecodeError:
            property_type_code = None
            locality_id = None
    else:
        property_type_code = None
        locality_id = None

    historical_price,property_yeald = fetch_investment_data(psmid, property_type_code, locality_id, locality)

    # fetch locality ratings
    locality_ratings = fetch_locality_ratings(locality_id)


    details["Locality Ratings"] = locality_ratings
    details["Historical Price (Locality)"] = historical_price
    details["Property Yield"] = property_yeald
    details["Property URL"] = url
    details["Property ID"] = property_id
    details["type"] = property_type
    details["Price"] = price
    details["BHK"] = bhk
    details["Total Area"] = total_area
    details["Name"] = name
    details["Description"] = description
    details["Rooms"] = rooms
    details["Floor Size"] = floor_size
    details["Latitude"] = latitude
    details["Longitude"] = longitude
    details["Locality"] = locality
    details["Region"] = region
    details["Project Photos"] = project_photos
    details["Locality Photos"] = locality_photos
    details["property photos"] = property_photos
    details["Furnishing"] = details.get("Furnishing", "Unfurnished")  # Default to Unfurnished if not found
    details["Status"] = details.get("Status", "Under Construction")  # Default to Under Construction if not found

    return details


def clean_property_data(data):
    def parse_price(price_str):
        if not price_str:
            return None
        price_str = price_str.replace("₹", "").replace(",", "").strip().lower()
        if "cr" in price_str:
            return float(price_str.replace("cr", "").strip()) * 1e7
        elif "lac" in price_str or "lakh" in price_str:
            return float(price_str.replace("lac", "").replace("lakh", "").strip()) * 1e5
        try:
            return float(price_str)
        except:
            return None

    def extract_numeric(value):
        if not value:
            return None
        match = re.search(r'[\d,.]+', value.replace(",", ""))
        return float(match.group()) if match else None

    cleaned_data = data.copy()

    # Clean Carpet Area
    cleaned_data["Carpet Area (sqft)"] = extract_numeric(cleaned_data.get("Carpet Area", ""))

    # Clean Price Per Sqft
    cleaned_data["Price Per Sqft"] = extract_numeric(cleaned_data.get("Price Per Sqft", ""))

    # Clean Total Area
    cleaned_data["Total Area (sqft)"] = extract_numeric(cleaned_data.get("Total Area", ""))

    # Clean Property Price
    cleaned_data["Price (INR)"] = parse_price(cleaned_data.get("Price", ""))

    yield_val = cleaned_data.get("Property Yield")
    try:
        cleaned_data["Property Yield (%)"] = float(yield_val)
    except (TypeError, ValueError):
        cleaned_data["Property Yield (%)"] = None

    raw_keys_to_remove = [
    "Carpet Area",
    "Price",
    "Total Area",
    "Property Yield",
    ]
    for key in raw_keys_to_remove:
        cleaned_data.pop(key, None)

    return cleaned_data


url = "https://www.magicbricks.com/propertyDetails/3-BHK-2520-Sq-ft-Multistorey-Apartment-FOR-Sale-Gota-in-Ahmedabad&id=4d423737323832383437"
property_data = scrape_property_details(url)
with open("property_details.json", "w") as outfile:
    property_data = clean_property_data(property_data)
    property_data["Property URL"] = url
    json.dump(property_data, outfile, indent=4)


links = []
with open("links.txt", "r") as file:
    links = file.readlines()
all_properties = []
for link in links[:10]:
    link = link.strip()
    if link:
        try:
            details = scrape_property_details(link)
            details = clean_property_data(details)
            details["Property URL"] = link
            all_properties.append(details)
            print(f"Scraped details for {link}")
        except Exception as e:
            print(f"Failed to scrape {link}: {e}")
            traceback.print_exc()

with open("property_details.json", "w") as outfile:
    json.dump(all_properties, outfile, indent=4)
