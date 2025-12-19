import search
from fastmcp import FastMCP
import httpx

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def scrape_page(url: str) -> str:
    """Scrape any web page and return its content in markdown format using jina.ai
    
    Args:
        url: The URL of the web page to scrape
        
    Returns:
        The page content in markdown format
    """
    # Use jina.ai's reader service to convert any URL to markdown
    jina_url = f"https://r.jina.ai/{url}"
    
    try:
        response = httpx.get(jina_url, timeout=30.0)
        response.raise_for_status()
        return response.text
    except httpx.HTTPError as e:
        return f"Error scraping page: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    
@mcp.tool
def minsearch(query: str, top_n: int = 5) -> dict:
    """Search markdown documentation files using minsearch
    
    Args:
        query: The search query string
        top_n: Number of top results to return (default: 5)
        
    Returns:
        Dictionary with query, total_results, and list of matching documents
    """
    try:
        return search.filesearch(query, top_n)
    except Exception as e:
        return {"error": str(e), "query": query}
    
if __name__ == "__main__":
    mcp.run()