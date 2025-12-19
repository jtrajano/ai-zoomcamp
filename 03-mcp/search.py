import json
from minsearch import Index


def load_documents():
    """Load documents from markdown_files_output.json"""
    with open('markdown_files_output.json', 'r', encoding='utf-8') as f:
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


def search(query, index, top_n=5):
    """
    Search for documents matching the query.
    
    Args:
        query: Search query string
        index: The minsearch Index object
        top_n: Number of top results to return (default: 5)
    
    Returns:
        List of top matching documents
    """
    # Boost content field more than file_path
    boost_dict = {"content": 3.0, "filename": 1.0}
    
    # Perform search
    results = index.search(
        query=query,
        boost_dict=boost_dict,
        num_results=top_n
    )
    
    return results


#def main():
    # Load documents
print("Loading documents...")
docs = load_documents()
print(f"Loaded {len(docs)} documents")

# Create and fit index
print("Creating index...")
index = create_index(docs)
print("Index created successfully")

# Example search
query = "demo"
print(f"\nSearching for: '{query}'")
print("-" * 80)

results = search(query, index, top_n=5)
    
    # Display results
for i, result in enumerate(results, 1):
    print(f"\n{i}. File: {result.get('filename', 'N/A')}")
    # print(f"   Score: {result.get('score', 'N/A'):.4f}")
    # Show first 200 characters of content
    content_preview = result.get('content', '')[:200].replace('\n', ' ')
    print(f"   Preview: {content_preview}...")

print("\n" + "-" * 80)
print(f"Total results: {len(results)}")
