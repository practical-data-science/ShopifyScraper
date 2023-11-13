# ShopifyScraper

ShopifyScraper is a Python package that scrapes data from Shopify. Unlike a regular web scraper, that needs to visit every page on a site, this package fetches Shopify's publicly visible `products.json` file, allowing you to scrape an entire store inventory in seconds.

When the commands below are run, ShopifyScraper will extract the store inventory and save the products and product variants to Pandas dataframes, from where you can access or analyse the data or write it to CSV or database. 

### Installation
To install ShopifyScraper, run the following command:

```bash
pip3 install git+https://github.com/practical-data-science/ShopifyScraper.git
```

### Usage

```python
from shopify_scraper import scraper

url = "https://yourshopifydomain.com"

products = scraper.get_products(url)
products.to_csv('products.csv', index=False)
print('Products: count=', len(products))


variants = scraper.get_variants(products)
variants.to_csv('variants.csv', index=False)
print('Variants: count=', len(variants))


images = scraper.get_images(products)
images.to_csv('images.csv', index=False)
print('Images: count=', len(images))
```

Note that variants has a many-to-one relationship with products, ON variant.product_id = product.id.

Note that images has a many-to-one relationship with products, ON image.product_id = product.id.
