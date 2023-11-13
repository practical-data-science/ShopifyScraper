"""
Shopify scraper
Description: Scrapes products from a Shopify store by parsing products.json and converting it to a pandas DataFrame.
Author: Matt Clarke
"""

import json
import pandas as pd
import requests

def get_json(url: str, page: int) -> str:
    """
    Get Shopify products.json from a store URL.

    Args:
        url (str): URL of the store.
        page (int): Page number of the products.json.
    Returns:
        products_json: Products.json from the store.
    """

    try:
        response = requests.get(f'{url}/products.json?limit=250&page={page}', timeout=5)
        products_json = response.text
        response.raise_for_status()
        return products_json

    except requests.exceptions.HTTPError as error_http:
        print("HTTP Error:", error_http)

    except requests.exceptions.ConnectionError as error_connection:
        print("Connection Error:", error_connection)

    except requests.exceptions.Timeout as error_timeout:
        print("Timeout Error:", error_timeout)

    except requests.exceptions.RequestException as error:
        print("Error: ", error)

def to_df(products_json: str) -> pd.DataFrame:
    """
    Convert products.json to a pandas DataFrame.

    Args:
        products_json (json): Products.json from the store.
    Returns:
        df: Pandas DataFrame of the products.json.
    """

    try:
        products_dict = json.loads(products_json)
        df = pd.DataFrame.from_dict(products_dict['products'])
        return df
    except Exception as e:
        print(e)

def get_products(url: str) -> pd.DataFrame:
    """
    Get all products from a store.

    Returns:
        df: Pandas DataFrame of the products.json.
    """

    results = True
    page = 1
    df = pd.DataFrame()

    while results:
        products_json = get_json(url, page)
        products_dict = to_df(products_json)

        if len(products_dict) == 0:
            break
        else:
            df = pd.concat([df, products_dict], ignore_index=True)
            page += 1

    df['url'] = f"{url}/products/" + df['handle']
    return df

def get_variants(products: pd.DataFrame) -> pd.DataFrame:
    """Get variants from a table of products.

    Args:
        products (pd.DataFrame): Pandas dataframe of products from get_products()

    Returns:
        variants (pd.DataFrame): Pandas dataframe of variants
    """

    products['id'].astype(int)
    df_variants = pd.DataFrame()

    for row in products.itertuples(index='True'):

        for variant in getattr(row, 'variants'):
            df_variants = pd.concat([df_variants, pd.DataFrame.from_records(variant, index=[0])])

    df_variants['id'].astype(int)
    df_variants['product_id'].astype(int)
    df_parent_data = products[['id', 'title', 'vendor']]
    df_parent_data = df_parent_data.rename(columns={'title': 'parent_title', 'id': 'parent_id'})
    df_variants = df_variants.merge(df_parent_data, left_on='product_id', right_on='parent_id')
    return df_variants

def json_list_to_df(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Return a Pandas dataframe based on a column that contains a list of JSON objects.

    Args:
        df (Pandas dataframe): The dataframe to be flattened.
        col (str): The name of the column that contains the JSON objects.

    Returns:
        Pandas dataframe: A new dataframe with the JSON objects expanded into columns.
    """

    rows = []
    for index, row in df[col].iteritems(): # FIXME: support removed in Pandas 2
        for item in row:
            rows.append(item)
    df = pd.DataFrame(rows)
    return df

def get_images(df_products: pd.DataFrame) -> pd.DataFrame:
    """Get images from a list of products.

    Args:
        df_products (pd.DataFrame): Pandas dataframe of products from get_products()

    Returns:
        images (pd.DataFrame): Pandas dataframe of images
    """

    return json_list_to_df(df_products, 'images')
