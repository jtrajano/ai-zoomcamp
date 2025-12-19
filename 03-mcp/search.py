import json
from pathlib import Path
from minsearch import Index


def load_documents():
    """Load documents from markdown_files_output.json"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    json_file = script_dir / 'markdown_files_output.json'
    
    with open(json_file, 'r', encoding='utf-8') as f:
        docs = json.load(f)
    return docs


def create_index(docs):
    """Create and fit minsearch index with the documents"""
    # Text fields to index - file_path and content
    text_fields = ["filename", "content"]
    
    # Create index
    index = Index(text_fields=text_fields)
    
    # Fit the index with documents
    index.fit(docs)
    
    return index


def filesearch(query, top_n=5):
    """
    Search for documents matching the query.

    Args:
        query: Search query string
        top_n: Number of top results to return (default: 5)

    Returns:
        Dictionary containing query, total results, and list of matching documents
    """
    docs = load_documents()
    
    # Create and fit index
    index = create_index(docs)
    
    # Boost content field more than file_path
    boost_dict = {"content": 3.0, "filename": 1.0}
        
    # Perform search
    results = index.search(
        query=query,
        boost_dict=boost_dict,
        num_results=top_n
    )
    
    # Format results for JSON output
    formatted_results = []
    for i, result in enumerate(results, 1):
        formatted_results.append({
            "rank": i,
            "filename": result.get('filename', 'N/A'),
            "content_preview": result.get('content', '')[:200].replace('\n', ' ') + "...",
            "full_content": result.get('content', '')
        })
    
    return {
        "query": query,
        "total_results": len(results),
        "results": formatted_results
    }
