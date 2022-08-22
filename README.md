# ShopifyScraper

ShopifyScraper is a Python package that scrapes data from Shopify. Unlike a regular web scraper, that needs to visit every page on a site, this package fetches Shopify's publicly visible `products.json` file, allowing you to scrape an entire store inventory in seconds.

When the commands below are run, ShopifyScraper will extract the store inventory and save the products and product variants to Pandas dataframes, from where you can access or analyse the data or write it to CSV or database. 

### Usage

```python
from shopify_scraper import scraper

url = "https://yourshopifydomain.com"

parents = scraper.get_products(url)
parents.to_csv('parents.csv', index=False)
print('Parents: ', len(parents))


children = scraper.get_variants(parents)
children.to_csv('children.csv', index=False)
print('Children: ', len(children))

```

