import os
import json
import requests
import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# URL of the website
url = 'http://localhost:3000'
# Directory to save files
download_dir = r'..\downloads'


def get_connection(self, url):
    session = Session()
    session.verify = False
    return session


def setup_elasticsearch():
    # Connect to our cluster
    es = Elasticsearch(
        [{'host': 'localhost', 'port': 9200, 'scheme': 'https'}],
        api_key="RURGM1FaQUJpX2hPNVowNkUxYk86dVlwU1BWTDVRamlUd2RVaU5BUXBYQQ==",
        verify_certs=False
    )
    return es

def index_file(es, file_name, content, file_url):
    # Index the file content and URL
    es.index(index='qualitätsmanagement', id=file_name, body={'content': content, 'url': file_url})

# Get the HTML content of the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links in the HTML content
links = soup.find_all('a')

# Filter the links to get only PDF and XLSX files
file_links = [link.get('href') for link in links if link.get('href', '').endswith(('.pdf', '.xlsx'))]

# Setup Elasticsearch
es = setup_elasticsearch()

# Download and save the files
for file_link in file_links:
    file_url = url + file_link
    file_response = requests.get(file_url, stream=True)
    file_name = os.path.join(download_dir, os.path.basename(file_link))

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'wb') as file:
        for chunk in file_response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    # Parse the downloaded files into JSON and index them into Elasticsearch
    if file_name.endswith('.pdf'):
        with pdfplumber.open(file_name) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            with open(file_name + '.json', 'w') as f:
                json_content = json.dumps(pages)
                f.write(json_content)
                index_file(es, file_name, json_content, file_url)
    elif file_name.endswith('.xlsx'):
        df = pd.read_excel(file_name)
        json_content = df.to_json()
        with open(file_name + '.json', 'w') as f:
            f.write(json_content)
            index_file(es, file_name, json_content, file_url)