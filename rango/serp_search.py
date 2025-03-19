import json
import requests
import os

# Define the base directory path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  

# Function to read the SerpAPI key from a file
def read_serpapi_key():
    key_path = os.path.join(BASE_DIR, "serpapi.key") 
    if not os.path.exists(key_path):
        raise OSError(f"SerpAPI key file not found: {key_path}")
    
    with open(key_path, "r") as key_file:
        return key_file.read().strip()

# Function to run a search query using SerpAPI
def run_query(search_terms):
    """
    Perform a Google search using SerpAPI.
    Documentation: https://serpapi.com/
    """
    serpapi_key = read_serpapi_key()
    search_url = 'https://serpapi.com/search'

    # Set request parameters
    params = {
        'q': search_terms,        # Search query
        'api_key': serpapi_key,   # API Key
        'engine': 'google',       # Search engine
        'num': 10                 # Number of results to return
    }

    # Send GET request to SerpAPI
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()

    # Parse and extract relevant information from the JSON response
    results = []
    if 'organic_results' in search_results:
        for result in search_results['organic_results']:
            results.append({
                'title': result.get('title', 'No Title'),
                'link': result.get('link', 'No URL'),
                'summary': result.get('snippet', 'No Snippet')
            })
    
    return results

# Test the search functionality
if __name__ == "__main__":
    query = "cake"
    search_results = run_query(query)

    # Print the top 5 search results
    for i, result in enumerate(search_results[:5]):
        print(f"{i+1}. {result['title']}\n   {result['link']}\n   {result['summary']}\n")