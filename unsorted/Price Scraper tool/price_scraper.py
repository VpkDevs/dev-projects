import requests
from bs4 import BeautifulSoup
from app import db
from app.models.models import Vape

def scrape_prices():
    # Example URLs of online retailers to scrape
    urls = [
        'https://example-vape-retailer.com',
        'https://another-vape-retailer.com'
    ]
    
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Logic to extract vape product prices from the HTML
            for vape in Vape.query.all():
                # Assuming the price is in a div with class 'price' and the model is in the text
                price_element = soup.find('div', class_='price', text=vape.model)
                if price_element:
                    lowest_price = float(price_element.text.strip('$'))
                    vape.lowest_price_found_online = lowest_price
                    db.session.add(vape)
            db.session.commit()
        else:
            print(f"Failed to retrieve data from {url}")

if __name__ == "__main__":
    scrape_prices()
