import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup

# Function to extract elements from a webpage
def extract_elements(url):
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # List of tags to extract
        tags_to_extract = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span']
        
        # Loop through each tag type and extract them
        for tag in tags_to_extract:
            elements = soup.find_all(tag)
            if elements:
                print(f"\nFound {len(elements)} '{tag}' elements:")
                for i, element in enumerate(elements, 1):
                    text = element.get_text(strip=True)  # Get text, remove extra whitespace
                    if text:  # Only print if there's actual text content
                        try:
                            # Try printing with UTF-8 encoding
                            print(f"{i}. {tag.upper()}: {text}".encode('utf-8').decode('utf-8'))
                        except UnicodeEncodeError:
                            # If encoding fails, replace problematic characters
                            safe_text = text.encode('utf-8', errors='replace').decode('utf-8')
                            print(f"{i}. {tag.upper()}: {safe_text}")
            else:
                print(f"\nNo '{tag}' elements found.")
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Replace this with the URL of the webpage you want to analyze
    webpage_url = "https://recruityard.com/"
    print(f"Extracting elements from: {webpage_url}\n")
    extract_elements(webpage_url)