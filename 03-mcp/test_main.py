import pytest
from unittest.mock import patch, Mock
import main


def test_add():
    """Test the add function"""
    result = main.add.fn(5, 3)
    assert result == 8
    
    result = main.add.fn(-5, 3)
    assert result == -2
    
    result = main.add.fn(0, 0)
    assert result == 0


def test_add_large_numbers():
    """Test add with large numbers"""
    result = main.add.fn(1000000, 2000000)
    assert result == 3000000


def test_add_negative_numbers():
    """Test add with negative numbers"""
    result = main.add.fn(-10, -20)
    assert result == -30


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


def test_minsearch_success():
    """Test successful minsearch query"""
    mock_result = {
        "query": "FastMCP",
        "total_results": 2,
        "results": [
            {
                "rank": 1,
                "filename": "README.md",
                "content_preview": "FastMCP is a framework...",
                "full_content": "FastMCP is a framework for building MCP servers"
            },
            {
                "rank": 2,
                "filename": "AGENTS.md",
                "content_preview": "Agent guidelines...",
                "full_content": "Agent guidelines for FastMCP"
            }
        ]
    }
    
    with patch('search.filesearch', return_value=mock_result):
        result = main.minsearch.fn("FastMCP")
        
        assert isinstance(result, dict)
        assert result["query"] == "FastMCP"
        assert result["total_results"] == 2
        assert len(result["results"]) == 2


def test_minsearch_with_top_n():
    """Test minsearch with custom top_n parameter"""
    mock_result = {
        "query": "test",
        "total_results": 3,
        "results": [{"rank": i} for i in range(1, 4)]
    }
    
    with patch('search.filesearch', return_value=mock_result) as mock_search:
        result = main.minsearch.fn("test", top_n=3)
        
        # Verify filesearch was called with correct parameters
        mock_search.assert_called_once_with("test", 3)
        assert result["total_results"] == 3


def test_minsearch_default_top_n():
    """Test minsearch with default top_n parameter"""
    mock_result = {
        "query": "test",
        "total_results": 1,
        "results": [{"rank": 1}]
    }
    
    with patch('search.filesearch', return_value=mock_result) as mock_search:
        result = main.minsearch.fn("test")
        
        # Verify filesearch was called with default top_n=5
        mock_search.assert_called_once_with("test", 5)


def test_minsearch_error_handling():
    """Test minsearch error handling"""
    with patch('search.filesearch', side_effect=Exception("Search failed")):
        result = main.minsearch.fn("test query")
        
        assert isinstance(result, dict)
        assert "error" in result
        assert result["error"] == "Search failed"
        assert result["query"] == "test query"


def test_minsearch_empty_results():
    """Test minsearch with no results"""
    mock_result = {
        "query": "nonexistent",
        "total_results": 0,
        "results": []
    }
    
    with patch('search.filesearch', return_value=mock_result):
        result = main.minsearch.fn("nonexistent")
        
        assert result["total_results"] == 0
        assert len(result["results"]) == 0


def test_minsearch_file_not_found_error():
    """Test minsearch when JSON file is not found"""
    with patch('search.filesearch', side_effect=FileNotFoundError("JSON file not found")):
        result = main.minsearch.fn("test")
        
        assert "error" in result
        assert "JSON file not found" in result["error"]


def test_minsearch_returns_dict():
    """Test that minsearch always returns a dict"""
    mock_result = {"query": "test", "total_results": 0, "results": []}
    
    with patch('search.filesearch', return_value=mock_result):
        result = main.minsearch.fn("test")
        assert isinstance(result, dict)
    
    # Even on error, should return dict
    with patch('search.filesearch', side_effect=Exception("error")):
        result = main.minsearch.fn("test")
        assert isinstance(result, dict)

