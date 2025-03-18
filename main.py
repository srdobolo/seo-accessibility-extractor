import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup

def extract_elements(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tags_to_extract = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span']
        
        for tag in tags_to_extract:
            # Find all elements of the tag type
            elements = soup.find_all(tag)
            if elements:
                # Track unique elements by tag and text
                seen = set()
                unique_elements = []
                
                for element in elements:
                    text = element.get_text(strip=True)
                    class_attr = element.get('class', [])
                    if text:  # Only process non-empty text
                        # Create a unique key: tag + text + class (as tuple)
                        key = (tag, text, tuple(class_attr))  # Tuple for hashability
                        if key not in seen:
                            seen.add(key)
                            unique_elements.append((tag, text, class_attr))
                
                if unique_elements:
                    print(f"\nFound {len(unique_elements)} unique '{tag}' elements:")
                    for i, (tag, text, class_attr) in enumerate(unique_elements, 1):
                        class_str = f" (class: {', '.join(class_attr)})" if class_attr else " (no class)"
                        try:
                            print(f"{i}. {tag.upper()}: {text}{class_str}")
                        except UnicodeEncodeError:
                            safe_text = text.encode('utf-8', errors='replace').decode('utf-8')
                            print(f"{i}. {tag.upper()}: {safe_text}{class_str}")
                else:
                    print(f"\nNo unique '{tag}' elements with text found.")
            else:
                print(f"\nNo '{tag}' elements found.")
                
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    webpage_url = "https://www.recruityard.com/"
    print(f"Extracting elements from: {webpage_url}\n")
    extract_elements(webpage_url)