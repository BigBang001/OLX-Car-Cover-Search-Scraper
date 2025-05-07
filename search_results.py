import requests
from bs4 import BeautifulSoup
import csv
import time

# URL for searching 'Car Cover' on OLX India
URL = "https://www.olx.in/items/q-car-cover"

# HTTP headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

def fetch_html(url):
    # Fetch the HTML content of the given URL.
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text

def parse_listings(html):
    # Parse the listings from OLX search results page.
    soup = BeautifulSoup(html, "html.parser")
    items = []

    listings = soup.find_all("li", class_="EIR5N")

    for listing in listings:
        try:
            title_tag = listing.find("span", class_="_2tW1I")
            price_tag = listing.find("span", class_="_89yzn")
            location_tag = listing.find("span", class_="_2tW1I _1h-2u")

            title = title_tag.text.strip() if title_tag else "N/A"
            price = price_tag.text.strip() if price_tag else "N/A"
            location = location_tag.text.strip() if location_tag else "N/A"

            items.append({
                "Title": title,
                "Price": price,
                "Location": location
            })
        except Exception as e:
            print(f"Error parsing listing: {e}")
            continue

    return items

def save_to_csv(items, filename="search_results.csv"):
    # Save the parsed items into a CSV file.
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Location"])
        writer.writeheader()
        writer.writerows(items)

    print(f"Saved {len(items)} results to {filename}")

def main():
    print("Fetching the OLX search results...")
    html = fetch_html(URL)
    print("Parsing listings...")
    items = parse_listings(html)
    print("Saving results...")
    save_to_csv(items)

if __name__ == "__main__":
    main()
