import requests


# Define the function to fetch data from Wikidata
def fetch_wikidata(params):
    url = "https://www.wikidata.org/w/api.php"
    try:
        response = requests.get(url, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"There was an error: {e}"


# Function to get the Wikidata ID from a Wikipedia page title
def get_wiki_id_from_page(page_title):
    params = {
        "action": "wbgetentities",
        "format": "json",
        "sites": "enwiki",
        "titles": page_title,
        "languages": "en",
        "prop": "redirects",
    }

    data = fetch_wikidata(params)

    # Handle cases where no entity is found or an error occurred
    if isinstance(data, str) or "entities" not in data or len(data["entities"]) == 0:
        return None

    entity_id = list(data["entities"].keys())[0]
    return entity_id


# Test the function with the given title
page_title = "William_T._Sherman"
entity_id = get_wiki_id_from_page(page_title)
print(entity_id)
