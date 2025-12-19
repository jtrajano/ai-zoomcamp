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

if __name__ == "__main__":
    mcp.run()