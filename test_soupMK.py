import unittest
from soupMK import SoupMaker
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock 

class TestSoupMK(unittest.TestCase):

    @patch('soupMK.requests.Session.get') #Mocking the requests.Session.get method to avoid real HTTP requests
    def test_makeSoup_success(self, mock_get):
        url = "http://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Hello</title></head><"
        mock_get.return_value = mock_response #Tells the mock to return our mock_response when called

        soup_maker = SoupMaker(set_url=url)
        soup = soup_maker.makeSoup()
        self.assertIsInstance(soup, BeautifulSoup) #Check if the returned object is an instance of BeautifulSoup
        self.assertEqual(soup.title.string, "Hello") #Check if the title is as expected
    
    def test_makeSoup_invalid_url(self):
        url = "http://invalid-url"
        soup_maker = SoupMaker(set_url=url)
        with self.assertRaises(Exception): #Expecting an exception to be raised for invalid URL
            soup_maker.makeSoup()

    def test_makeSoup_no_url(self):
        soup_maker = SoupMaker()
        with self.assertRaises(ValueError):
            soup_maker.makeSoup()

    @patch('soupMK.requests.Session.get')
    def test_makeSoup_non_200_status(self, mock_get):
        url = "https://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 9030
        mock_response.text = "<html><head><title>Hello</title></head><"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url=url)
        with self.assertRaises(Exception):
            soup_maker.makeSoup()
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_custom_headers(self, mock_get):
        url = "http://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Custom Header</title></head><"
        mock_get.return_value = mock_response

        custom_headers = {
            "User-Agent": "CustomAgent/1.0",
            "Accept": "text/html"
        }
        soup_maker = SoupMaker(set_url=url, headers=custom_headers)
        self.assertEqual(soup_maker.headers, custom_headers)
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_empty_content(self, mock_get):
        url = "http://example.com"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_get.return_value = mock_response
        
        soup_maker = SoupMaker(set_url=url)
        soup = soup_maker.makeSoup()
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.text, "")

    
