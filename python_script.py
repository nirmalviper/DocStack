import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- CONFIG ---
API_BASE_URL = "HTTPS://YOUR_INSTALLATION_PATH/api/"
API_TOKEN_ID = "YOUR_TOKEN_ID"  # Replace with your actual token ID
API_TOKEN_SECRET = "YOUR_TOKEN_SECRET"  # Replace with your actual token secret

ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))  # your local folder path

HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + API_TOKEN_ID + ':' + API_TOKEN_SECRET,
}


# --- FUNCTIONS ---

def make_api_request(method, endpoint, json_data=None, retries=3):
    """Generic API request handler with retries"""
    url = urljoin(API_BASE_URL, endpoint)
    for attempt in range(retries):
        try:
            response = requests.request(
                method,
                url,
                json=json_data,
                headers=HEADERS,
                # verify=False  # Disable SSL verification for self-signed certs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                raise
            time.sleep(2)  # Wait before retrying

def create_shelf(name):
    """Create a new shelf and return its ID"""
    print(f"Creating shelf: {name}")
    response = make_api_request("POST", "shelves", {"name": name})
    shelf_id = response.get("id")
    print(f"Created shelf with ID: {shelf_id}")
    return shelf_id

def update_shelf_with_books(shelf_id, name, description_html, book_ids):
    """Update shelf and assign books to it"""
    print(f"Updating shelf {shelf_id} with books {book_ids}")
    response = make_api_request("PUT", f"shelves/{shelf_id}", {
        "name": name,
        "description_html": description_html,
        "books": book_ids
    })
    print("Shelf updated.")

def create_book(name, shelf_id=None):
    """Create a new book and optionally add to shelf"""
    print(f"Creating book: {name}")
    response = make_api_request("POST", "books", {"name": name})
    book_id = response.get("id")
    print(f"Created book with ID: {book_id}")
    
    # # Add to shelf if specified
    # if shelf_id:
    #     print(f"Adding book {book_id} to shelf {shelf_id}")
    #     make_api_request("POST", f"shelves/{shelf_id}/books/{book_id}")
    
    return book_id

def create_chapter(book_id, name):
    """Create a new chapter in a book"""
    print(f"Creating chapter: {name}")
    response = make_api_request("POST", "chapters", {
        "book_id": book_id,
        "name": name
    })
    chapter_id = response.get("id")
    print(f"Created chapter with ID: {chapter_id}")
    return chapter_id

def create_page(book_id, chapter_id, name, html_content):
    """Create a new page with HTML content and filtered tags"""
    print(f"Creating page: {name}")
    
    # Clean HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    clean_html = str(soup)
    
    # Generate tags: only words 4+ characters
    words = name.replace("-", " ").replace("_", " ").split()
    tags = [{"name": word.strip()} for word in words if len(word.strip()) >= 4]
    
    make_api_request("POST", "pages", {
        "book_id": book_id,
        "chapter_id": chapter_id,
        "name": name,
        "html": clean_html,
        "markdown": "",
        "tags": tags
    })
    
    print(f"Created page: {name} with tags: {[tag['name'] for tag in tags]}")


# --- MAIN EXECUTION ---

def main():
    print("Starting BookStack import...")

    try:
        test_response = make_api_request("GET", "shelves")
        print("API connection successful")
    except Exception as e:
        print(f"API connection failed: {e}")
        return

    # Process each shelf
    for shelf_name in os.listdir(ROOT_FOLDER):
        shelf_path = os.path.join(ROOT_FOLDER, shelf_name)
        if not os.path.isdir(shelf_path):
            continue

        shelf_id = create_shelf(shelf_name)
        book_ids = []

        # Process each book in shelf
        for book_name in os.listdir(shelf_path):
            book_path = os.path.join(shelf_path, book_name)
            if not os.path.isdir(book_path):
                continue

            book_id = create_book(book_name)
            book_ids.append(book_id)

            # Process each HTML file in book
            for html_file in sorted(os.listdir(book_path)):
                if not html_file.lower().endswith(".html"):
                    continue

                chapter_title = os.path.splitext(html_file)[0]
                chapter_id = create_chapter(book_id, chapter_title)

                file_path = os.path.join(book_path, html_file)
                with open(file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()

                create_page(book_id, chapter_id, chapter_title, html_content)
                time.sleep(1)  # Avoid rate limit

        # Now update the shelf with books
        description_html = f"<p>Shelf for {shelf_name} with imported books</p>"
        update_shelf_with_books(shelf_id, shelf_name, description_html, book_ids)

    print("✅ Import completed successfully!")


if __name__ == "__main__":
    main()