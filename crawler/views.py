from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import os

from openai import OpenAI
from account.models import FileInformation


def download_files(request):
    openai = OpenAI("your_openai_api_key")
    url = ('http://localhost:63342/unicrawler/templates/index.html?_ijt=kq6vhqgbkshh2j9odqbbo87oe6&_ij_reload'
           '=RELOAD_ON_SAVE')  # the url of the website you want to crawl
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.select("a[href$='.pdf'], a[href$='.xls']"):
        file_url = link['href']
        file_name = os.path.join('downloads', os.path.basename(file_url))
        with open(file_name, 'wb') as file:
            response = requests.get(file_url)
            file.write(response.content)

        # Analyze the file with OpenAI
        with open(file_name, 'rb') as file:
            analysis = openai.Analysis.create(
                model="text-davinci-002",
                file=file,
                tasks=["classification", "extraction"]
            )

        # Store the file information in the database
        FileInformation.objects.create(
            subject=analysis.results["classification"]["answer"],
            tags=analysis.results["extraction"]["answer"],
            download_url=file_url
        )
    return HttpResponse('Files downloaded successfully')

