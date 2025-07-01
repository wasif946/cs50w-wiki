import markdown2 # Make sure you have installed this library: pip install markdown2
import re

def convert_markdown_to_html(markdown_text):
    """
    Converts a given Markdown text string into an HTML string.

    This function uses the 'markdown2' library to perform the conversion.
    It's particularly useful for rendering user-submitted wiki entries
    that are written in Markdown format.
    """
    # Use extras like 'fenced-code-blocks' for better code block rendering
    # and 'tables' for markdown tables.
    html_content = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables"])
    return html_content

def search_entries(query, entries):
    """
    Searches a list of entries for a given query.
    Returns a list of entries whose titles exactly match the query (case-insensitive)
    or whose titles contain the query as a substring (case-insensitive).

    Args:
        query (str): The search term.
        entries (list): A list of strings, where each string is an entry title.

    Returns:
        list: A list of matching entry titles.
    """
    matching_entries = []
    query_lower = query.lower()

    # First, check for exact matches (case-insensitive)
    for entry in entries:
        if entry.lower() == query_lower:
            return [entry] # If exact match, return only that entry

    # If no exact match, find entries that contain the query as a substring
    for entry in entries:
        if query_lower in entry.lower():
            matching_entries.append(entry)

    return matching_entries

# Example of how you might use this (optional, for testing):
if __name__ == "__main__":
    print("--- Markdown to HTML Conversion Test ---")
    markdown_example = """
# Hello World

This is a **bold** paragraph.

- Item 1
- Item 2

```python
def greet(name):
    print(f"Hello, {name}!")
```

| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
"""
    html_output = convert_markdown_to_html(markdown_example)
    print(html_output)

    print("\n--- Search Entries Test ---")
    all_entries = ["Python", "Django", "HTML", "CSS", "JavaScript", "Python Basics"]
    
    # Exact match
    results1 = search_entries("python", all_entries)
    print(f"Searching for 'python': {results1}") # Expected: ['Python']

    # Substring match
    results2 = search_entries("script", all_entries)
    print(f"Searching for 'script': {results2}") # Expected: ['JavaScript']

    # No match
    results3 = search_entries("Flask", all_entries)
    print(f"Searching for 'Flask': {results3}") # Expected: []

    # Case-insensitive substring
    results4 = search_entries("HTML", all_entries)
    print(f"Searching for 'HTML': {results4}") # Expected: ['HTML']
