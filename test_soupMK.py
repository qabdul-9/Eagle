import unittest
import requests
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
    
    @patch('soupMK.validators.url')
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_timeout_error(self, mock_get, mock_validator):
        url = "https://example.com"
        mock_validator.return_value = True
        mock_get.side_effect = requests.RequestException("Requests timed out")

        soup_maker = SoupMaker(set_url=url)
        with self.assertRaises(Exception) as context:
            soup_maker.makeSoup()
        self.assertIn("An error occurred while fetching the page:", str(context.exception))

    @patch('soupMK.requests.Session.get')
    def test_validate_url(self, mock_get):
        url = "http://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Hello</title></head><"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url=url)
        self.assertTrue(soup_maker.is_vaild_url(url))
    
    @patch('soupMK.validators.url')
    @patch('soupMK.requests.Session.get')
    def test_validate_url_invalid(self, mock_get, mock_validator):
        url = "invalid-url"
        mock_validator.return_value = False

        soup_maker = SoupMaker(set_url=url)
        self.assertFalse(soup_maker.is_vaild_url(url))

    def test_is_vaild_url_static(self):
        valid_url = "http://example.com"
        invalid_url = "invalid-url"
        self.assertTrue(SoupMaker().is_vaild_url(valid_url))
        self.assertFalse(SoupMaker().is_vaild_url(invalid_url))
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_default_headers(self, mock_get):
        url = "http://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Hello</title></head></html>"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url=url)
        soup_maker.makeSoup()

        called_headers = mock_get.call_args[1]['headers']
        self.assertEqual(called_headers, soup_maker.headers)
        self.assertIn("User-Agent", called_headers)
        self.assertIn("Accept", called_headers)

    @patch('soupMK.requests.Session.get')
    def test_makeSoup_empty_header(self, mock_get):
        url = "https://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 403 #Forbidden response code is usually sent by Amazon, Google, etc. This means the server refused acccess.
        mock_response.text = "<html><head><title>This should not return</title></head></html>"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url=url, headers="")
        with self.assertRaises(Exception):
            soup_maker.makeSoup()
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_extract_title(self, mock_get):
        url = "https://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><Title>Extract this title.</title></head></html>"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url=url)
        soup = soup_maker.makeSoup()
        
        self.assertEqual("Extract this title.",soup.text)
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_extract_image(self, mock_get):
        url = "https://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><Title>Extract this image.</title><body>" \
                            "<img src='stock_image.png'></body></head></html>"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url=url)
        soup = soup_maker.makeSoup()
        
        img_tag = soup.find('img')
        self.assertEqual(img_tag['src'], "stock_image.png")
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_no_image_element(self,mock_get):
        url = "https://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><Title>Extract this image.</title><body>" \
                            "</body></head></html>"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url=url)
        soup = soup_maker.makeSoup()
        
        self.assertIsNone(soup.find('img'))
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_invalid_keyword(self, mock_get):
        url = "https://example.com/s?k="
        keyword = "invalid#/key!"
        test_url = url + keyword
        mock_response = MagicMock()
        mock_response.status_code = 400 #Bad Request
        mock_response.text = "Do not return"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url = test_url)
        with self.assertRaises(Exception):
            soup_maker.makeSoup()

    @patch('soupMK.requests.Session.get')
    def test_makeSoup_override_constructor(self, mock_get):
        constructor_url = "https://constructor.com"
        new_url = "https://newUrl.com"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text =  "<html><head><Title>New Url.</title><body>" \
                            "</body></head></html>"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url = constructor_url)
        soup = soup_maker.makeSoup(new_url)
        self.assertEqual("New Url.", soup.text)

    @patch('soupMK.requests.Session.get')
    def test_makeSoup_no_title_tag(self, mock_get):
        url = "https://sample.com"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>This is a paragraph.</p></body></html>"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url = url)
        soup = soup_maker.makeSoup()

        self.assertIsNone(soup.find('title'))
        self.assertIn('This is a paragraph', soup.text)
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_valid_keyword(self, mock_get):
        url = "https://sample.com/s?k="
        keyword = "red+shirt"
        fe = url+keyword

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>There exists a red shirt.</p></body></html>"
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url= fe)
        soup = soup_maker.makeSoup()

        self.assertEqual('There exists a red shirt.', soup.text)
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_multiple_images(self, mock_get):
        url = "https://sample.com"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <img src="red.png">
                <img src="blue.png">
                <img src="green.png"> 
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        soup_maker = SoupMaker(set_url = url)
        soup = soup_maker.makeSoup()

        images = soup.find_all('img')
        expected_src = ["red.png", "blue.png", "green.png"]
        src_list = []
        for image in images:
            src_list.append(image['src'])

        self.assertEqual(src_list, expected_src)

    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_with_relative_links(self, mock_get):
        """Test if relative <a> links are parsed correctly."""
        url = "https://example.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html><body><a href="/about">About Us</a></body></html>
        """
        mock_get.return_value = mock_response
        soup = SoupMaker(set_url=url).makeSoup()
        self.assertEqual(soup.find('a')['href'], "/about")
   
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_with_special_characters(self, mock_get):
        """Ensure HTML entities are decoded properly."""
        url = "https://specialchars.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>5 &lt; 10 &amp; 7 &gt; 2</p></body></html>"
        mock_get.return_value = mock_response
        soup = SoupMaker(set_url=url).makeSoup()
        self.assertIn("5 < 10 & 7 > 2", soup.text)  

    @patch('soupMK.requests.Session.get')
    def test_makeSoup_with_nested_elements(self, mock_get):
        """Test nested HTML tags parsing correctly."""
        url = "https://nested.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><div><p><span>Hello</span></p></div></body></html>"
        mock_get.return_value = mock_response
        soup = SoupMaker(set_url=url).makeSoup()
        self.assertEqual(soup.find('span').text, "Hello")
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_with_comment_tags(self, mock_get):
        """Ensure HTML comments are ignored in the text output."""
        url = "https://comments.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><!-- Hidden comment --><p>Visible</p></body></html>"
        mock_get.return_value = mock_response
        soup = SoupMaker(set_url=url).makeSoup()
        self.assertNotIn("Hidden comment", soup.text)
        self.assertIn("Visible", soup.text)

    @patch('soupMK.requests.Session.get')
    def test_makeSoup_with_meta_tags(self, mock_get):
        """Check if meta tag content can be found."""
        url = "https://meta.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html><head><meta name='description' content='Test description'></head></html>
        """
        mock_get.return_value = mock_response
        soup = SoupMaker(set_url=url).makeSoup()
        meta = soup.find('meta', attrs={'name': 'description'})
        self.assertEqual(meta['content'], 'Test description')
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_with_redirect_page(self, mock_get):
        """Simulate a redirect (302) and ensure it raises an error."""
        url = "https://redirect.com"
        mock_response = MagicMock()
        mock_response.status_code = 302
        mock_response.text = "<html><body>Redirecting...</body></html>"
        mock_get.return_value = mock_response
        with self.assertRaises(Exception):
            SoupMaker(set_url=url).makeSoup()
    
    @patch('soupMK.requests.Session.get')
    def test_makeSoup_with_unicode_characters(self, mock_get):
        """Ensure Unicode characters (like emojis) are parsed correctly."""
        url = "https://unicode.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>Emoji test 😀🔥</p></body></html>"
        mock_get.return_value = mock_response
        soup = SoupMaker(set_url=url).makeSoup()
        self.assertIn("😀", soup.text)

    @patch('soupMK.requests.Session.get')
    def test_makeSoup_with_large_html(self, mock_get):
        """Simulate parsing a very large HTML string."""
        url = "https://largepage.com"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>" + "<p>Test</p>" * 5000 + "</body></html>"
        mock_get.return_value = mock_response
        soup = SoupMaker(set_url=url).makeSoup()
        self.assertTrue(len(soup.find_all('p')) == 5000)
if __name__ == '__main__':
    unittest.main()

