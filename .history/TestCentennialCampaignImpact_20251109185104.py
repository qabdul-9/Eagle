import unittest
from unittest.mock import patch, Mock
from centennial_scraper import get_centennial_campaign_impact

class TestCentennialCampaignImpact(unittest.TestCase):

    @patch('centennial_scraper.requests.get')
    def test_returns_list(self, mock_get):
        mock_response = Mock()
        mock_response.text = "<html><body>Test content</body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_centennial_campaign_impact()
        self.assertIsInstance(result, list)

    @patch('centennial_scraper.requests.get')
    def test_returns_non_empty_list(self, mock_get):
        mock_response = Mock()
        mock_response.text = "<html><body><p>Campaign Impact</p><p>Details here</p></body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_centennial_campaign_impact()
        self.assertGreater(len(result), 0)

    @patch('centennial_scraper.requests.get')
    def test_all_items_are_strings(self, mock_get):
        mock_response = Mock()
        mock_response.text = "<html><body><p>Line 1</p><p>Line 2</p></body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_centennial_campaign_impact()
        for item in result:
            self.assertIsInstance(item, str)



if __name__ == '__main__':
    unittest.main()
