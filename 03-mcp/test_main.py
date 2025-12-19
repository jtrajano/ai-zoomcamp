import pytest
from unittest.mock import patch, Mock
import main


def test_scrape_page_success():
    """Test successful page scraping"""
    mock_response = Mock()
    mock_response.text = "# Example Page\n\nThis is markdown content."
    mock_response.raise_for_status = Mock()
    
    with patch('httpx.get', return_value=mock_response) as mock_get:
        result = main.scrape_page.fn("https://datatalks.club")
        
        # Verify jina.ai URL was called
        mock_get.assert_called_once_with("https://r.jina.ai/https://datatalks.club", timeout=30.0)
        
        # Verify the result is the markdown content
        assert result == "# Example Page\n\nThis is markdown content."
        mock_response.raise_for_status.assert_called_once()


def test_scrape_page_http_error():
    """Test handling of HTTP errors"""
    import httpx
    
    with patch('httpx.get', side_effect=httpx.HTTPError("404 Not Found")):
        result = main.scrape_page.fn("https://datatalks.club/notfound")
        
        assert "Error scraping page:" in result
        assert "404 Not Found" in result


def test_scrape_page_timeout_error():
    """Test handling of timeout errors"""
    import httpx
    
    with patch('httpx.get', side_effect=httpx.TimeoutException("Request timeout")):
        result = main.scrape_page.fn("https://slow-example.com")
        
        assert "Error scraping page:" in result
        assert "Request timeout" in result


def test_scrape_page_unexpected_error():
    """Test handling of unexpected errors"""
    with patch('httpx.get', side_effect=Exception("Unexpected error occurred")):
        result = main.scrape_page.fn("https://datatalks.club")
        
        assert "Unexpected error:" in result
        assert "Unexpected error occurred" in result


def test_scrape_page_with_various_urls():
    """Test scraping with different URL formats"""
    mock_response = Mock()
    mock_response.text = "# Test Content"
    mock_response.raise_for_status = Mock()
    
    test_urls = [
        "https://github.com/user/repo",
        "https://docs.python.org/3/",
        "http://example.com/path?query=value",
    ]
    
    with patch('httpx.get', return_value=mock_response) as mock_get:
        for url in test_urls:
            result = main.scrape_page.fn(url)
            assert result == "# Test Content"
            
            # Verify the URL was properly formatted for jina.ai
            expected_jina_url = f"https://r.jina.ai/{url}"
            call_args = mock_get.call_args_list[-1]
            assert call_args[0][0] == expected_jina_url


def test_scrape_page_returns_string():
    """Test that scrape_page always returns a string"""
    mock_response = Mock()
    mock_response.text = "Test content"
    mock_response.raise_for_status = Mock()
    
    with patch('httpx.get', return_value=mock_response):
        result = main.scrape_page.fn("https://datatalks.club")
        assert isinstance(result, str)
        assert len(result) > 0
