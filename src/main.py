import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Example: extract all table data
    tables = pd.read_html(html)
    return tables

def main():
    url = 'https://example.com'  # Replace with your target URL
    html = fetch_webpage(url)
    tables = parse_html(html)
    for i, table in enumerate(tables):
        print(f'Table {i+1}:')
        print(table.head())

if __name__ == '__main__':
    main()
