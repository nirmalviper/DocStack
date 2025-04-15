import os
import requests
import urllib3

# --- CONFIGURATION ---
API_BASE_URL = "http://localhost/bookstack/public/api"
API_TOKEN_ID = "oXtOjW4tRVf3wPoLA2fsMx11fUSu5RRt"
API_TOKEN_SECRET = "PsoWaunYKYSGZaWu4tntg6uNi8xdYwDi"
ROOT_FOLDER = os.path.dirname(os.path.abspath(__file__))  # ← Update this to your root folder path

HEADERS = {
    "Authorization": f"Token {API_TOKEN_ID}:{API_TOKEN_SECRET}",
    "Content-Type": "application/json"
}

# Disable HTTPS warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# --- API FUNCTIONS ---
def create_shelf(name):
    print(f"Creating shelf: {name}")
    res = requests.post(f"{API_BASE_URL}/shelves", json={"name": name}, headers=HEADERS, verify=False)
    res.raise_for_status()
    return res.json()["id"]

def create_book(name, shelf_id):
    print(f"  Creating book: {name}")
    res = requests.post(f"{API_BASE_URL}/books", json={"name": name, "shelf_id": shelf_id}, headers=HEADERS, verify=False)
    res.raise_for_status()
    return res.json()["id"]

def create_page(name, html_content, book_id):
    print(f"    Creating page: {name}")
    res = requests.post(f"{API_BASE_URL}/pages", json={
        "book_id": book_id,
        "name": name,
        "html": html_content
    }, headers=HEADERS, verify=False)
    res.raise_for_status()
    return res.json()["id"]


# --- MAIN FUNCTION ---
def upload_books_from_folder(root_folder):
    shelf_name = os.path.basename(root_folder)
    shelf_id = create_shelf(shelf_name)

    for book_folder in os.listdir(root_folder):
        book_path = os.path.join(root_folder, book_folder)
        if not os.path.isdir(book_path):
            continue

        book_id = create_book(book_folder, shelf_id)

        for file_name in sorted(os.listdir(book_path)):
            if file_name.endswith(".html"):
                file_path = os.path.join(book_path, file_name)
                with open(file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                page_title = os.path.splitext(file_name)[0].replace("-", " ").replace("_", " ").title()
                create_page(page_title, html_content, book_id)


# --- EXECUTE ---
if __name__ == "__main__":
    upload_books_from_folder(ROOT_FOLDER)
