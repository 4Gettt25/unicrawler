from unittest.mock import patch, Mock
from django.contrib.sites import requests
from django.test import TestCase
from crawler import views  # replace with your actual class


def crawler_successfully_downloads_files(self):
    response = self.crawler.download_files()
    self.assertEqual(response.status_code, 200)
    self.assertIn('Files downloaded successfully', response.content.decode())


def crawler_handles_no_files_to_download(self):
    with patch('requests.get', return_value=Mock(status_code=200, text='<html></html>')):
        response = self.crawler.download_files()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Files downloaded successfully', response.content.decode())


def crawler_handles_request_exception(self):
    with patch('requests.get', side_effect=requests.exceptions.RequestException):
        with self.assertRaises(requests.exceptions.RequestException):
            self.crawler.download_files()


def crawler_handles_openai_analysis_error(self):
    with patch('openai.Analysis.create', side_effect=Exception):
        with self.assertRaises(Exception):
            self.crawler.download_files()
