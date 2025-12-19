import os
import json
import sys
from pathlib import Path


def read_markdown_files(root_dir="."):
    """
    Read all .md and .mdx files from the given directory and subdirectories.
    
    Args:
        root_dir: The root directory to start searching from (default: current directory)
    
    Returns:
        List of dictionaries containing file_path and content
    """
    # root_dir="C:\\Users\\Jeff\\Downloads\\fastmcp-main\\fastmcp-main"
    results = []
    
    # Convert to absolute path
    root_path = Path(root_dir).resolve()
    
    # Walk through all directories
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            # Check if file has .md or .mdx extension
            if filename.endswith('.md') or filename.endswith('.mdx'):
                file_path = os.path.join(dirpath, filename)
                
                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    results.append({
                        "file_path": file_path,
                        "content": content
                    })
                except Exception as e:
                    # If there's an error reading a file, log it but continue
                    print(f"Error reading {file_path}: {e}", file=sys.stderr)
    
    return results


def main():
    # Get directory from command line argument or use current directory
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "."
    
    # Read all markdown files
    markdown_files = read_markdown_files(directory)
    
    # Output filename
    output_file = "markdown_files_output.json"
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(markdown_files, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to {output_file}")
    print(f"Total files found: {len(markdown_files)}")


if __name__ == "__main__":
    main()
