import requests

# Function to fetch data from Wikidata
def fetch_wikidata(params):
    wikidata_url = "https://www.wikidata.org/w/api.php"
    try:
        response = requests.get(wikidata_url, params=params)
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"There was an error: {e}"

# Function to resolve Wikipedia redirects
def resolve_redirect(title):
    wikipedia_api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": title,
        "redirects": 1,
        "format": "json"
    }
    response = requests.get(wikipedia_api_url, params=params)
    data = response.json()

    # Check if a redirect exists and get the final title
    if 'redirects' in data['query']:
        final_title = data['query']['redirects'][0]['to']
    else:
        final_title = title  # No redirect, use the original title

    return final_title

# Function to get the Wikidata ID from a Wikipedia page title
def get_wiki_id_from_page(page_title):
    final_title = resolve_redirect(page_title)  # Resolve redirects first
    params = {
        "action": "wbgetentities",
        "format": "json",
        "sites": "enwiki",
        "titles": final_title,
        "languages": "en",
        "redirects": "yes",
    }
    data = fetch_wikidata(params)
    if isinstance(data, str) or 'entities' not in data or len(data['entities']) == 0:
        return None

    entity_id = list(data['entities'].keys())[0]
    return entity_id

# Example usage
page_title = "William_T._Sherman"
page_title = "Tina_Turner"
entity_id = get_wiki_id_from_page(page_title)
print("Wikidata ID:", entity_id)
