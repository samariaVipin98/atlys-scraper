import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from repo.notification.notification import send_email
from database.models import Product, User
from schema.scraper.scraper_request import ScraperRequest
from repo.utils.utils import retry


def process_data(db, request: ScraperRequest, current_user: User):
    scraper = Scraper(pages=request.pages, proxy=request.proxy)
    data = scraper.scrape(db)
    send_email(current_user.email, "Scraping Complete", str(data))

class Scraper:
    def __init__(self, pages: int, max_retries: Optional[int] = 3, proxy: Optional[str] = None):
        self.pages = pages
        self.proxy = proxy
        self.base_url = "https://dentalstall.com/shop"
        self.max_retries = max_retries
        self.fetch_page = retry(max_retries=self.max_retries, delay=5)(self.fetch_page)
    
    def fetch_page(self, url: str) -> str:
        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        return response.text

    def scrape(self, db) -> List[Dict]:
        inserted_count = 0
        duplicate_count = 0
        updated_count = 0

        for page in range(1, self.pages + 1):
            if page == 1:
                url = f"{self.base_url}"
            else:
                url = f"{self.base_url}/page/{page}"
            html = self.fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            for product in soup.select(".product"):
                title_element = product.select_one(".woo-loop-product__title a")
                price_element = product.select_one(".woocommerce-Price-amount")
                image_element = product.select_one(".mf-product-thumbnail img")

                # Extract title
                title = title_element.text.strip() if title_element else "No title"

                # Extract price
                price_text = price_element.text.strip().replace("₹", "") if price_element else "0"
                try:
                    price = float(price_text.replace(",", ""))  # Remove commas and convert to float
                except ValueError:
                    price = 0.0

                # Extract image URL
                image_url = image_element["data-lazy-src"] if image_element else "No image"
                image_path = self.download_image(image_url, title)

                # Check if product exists
                product = db.query(Product).filter(Product.title == title).first()

                if product:
                    # If product exists, check for price change
                    if product.price != price:
                        product.price = price
                        db.commit()
                        updated_count += 1
                    else:
                        duplicate_count += 1
                
                else:
                    # Insert new product
                    new_product = Product(title=title, price=price, image_url=image_path)
                    db.add(new_product)
                    db.commit()
                    inserted_count += 1
        
        return {'inserted_count': inserted_count, 'duplicate_count': duplicate_count, 'updated_count': updated_count}

    
    def download_image(self, image_url: str, title: str) -> str:
        # Create a directory for images if it doesn't exist
        directory = '../../images'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Construct the image path
        # Sanitize title to create a valid filename
        safe_filename = ''.join(c for c in title if c.isalnum() or c in (' ', '_', '-'))  # Keep only valid characters
        filename = f"{safe_filename}.jpg"
        image_path = os.path.join(directory, filename)
        
        # Download and save the image
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Check for HTTP errors
            with open(image_path, 'wb') as file:
                file.write(response.content)
        except Exception as e:
            print(f"Failed to download image {image_url}: {e}")
            image_path = ''  # Return an empty path or handle the error appropriately
        
        return image_path
