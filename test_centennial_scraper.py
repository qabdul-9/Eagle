import unittest
import centennial_scraper
from unittest.mock import patch, MagicMock

class TestCentennialScraper(unittest.TestCase):
    def setUp(self):
        self.sample_html = """
        <html>
            <body>
                <h1>Centennial Campaign</h1>
                <p>The impact of our centennial campaign is significant.</p>
                <p>We have raised funds for various projects.</p>
            </body>
        </html>
        """
    @patch('centennial_scraper.requests.get')
    def test_get_centennial_campaign_impact_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_html
        mock_get.return_value = mock_response

        result = centennial_scraper.get_centennial_campaign_impact(keyword="impact")
        self.assertIn("The impact of our centennial campaign is significant.", result)

    @patch('centennial_scraper.requests.get')
    def test_get_centennial_campaign_impact_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_html
        mock_get.return_value = mock_response

        result = centennial_scraper.get_centennial_campaign_impact(keyword="nonexistent")
        self.assertTrue(len(result) <= 500)

    @patch('centennial_scraper.requests.get')
    def test_get_centennial_campaign_impact_empty_html(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_get.return_value = mock_response

        result = centennial_scraper.get_centennial_campaign_impact(keyword="impact")
        self.assertEqual(result, "")

    @patch('centennial_scraper.requests.get')
    def test_get_centennial_campaign_impact_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = centennial_scraper.get_centennial_campaign_impact(keyword="impact")
        self.assertEqual(result, "")

    @patch('centennial_scraper.requests.get')
    def test_get_centennial_campaign_impact_no_url(self):
        result = centennial_scraper.get_centennial_campaign_impact(url="")
        self.assertEqual(result, "")

    @patch('centennial_scraper.requests.get')
    def test_get_centennial_campaign_impact_no_keyword(self):
        result = centennial_scraper.get_centennial_campaign_impact(keyword="")
        self.assertEqual(result, "")

    def test_search_page_found(self):
        with patch('centennial_scraper.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = self.sample_html
            mock_get.return_value = mock_response

            result = centennial_scraper.search_page(keyword="impact")
            self.assertIn("The impact of our centennial campaign is significant.", result)

    def test_search_page_not_found(self):
        with patch('centennial_scraper.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = self.sample_html
            mock_get.return_value = mock_response

            result = centennial_scraper.search_page(keyword="nonexistent")
            self.assertTrue(len(result) <= 500)

    def test_search_page_empty_html(self):
        with patch('centennial_scraper.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = ""
            mock_get.return_value = mock_response

            result = centennial_scraper.search_page(keyword="impact")
            self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()