# imports
import requests
import time
import json

# Download flags (DEBUG)
dl_cb = False
dl_cl = False

# API endpoint for bulk cards (Oracle cards)
bulk_uri = "https://api.scryfall.com/bulk-data/oracle-cards"

# API request wait time
wait_time = 1

# Cardbase filename
filename = "cardbase.json"

if dl_cb:
    # Add delay before any requests to prevent excessive requests
    time.sleep(wait_time)

    # Make a request for bulk cards
    print(f"Making bulk request @ [{bulk_uri}]")
    bulk_response = requests.get(bulk_uri)

    # Get the bulk download uri
    download_uri = bulk_response.json()["download_uri"]

    # Add delay before any requests to prevent excessive requests
    time.sleep(wait_time)

    # Get the cardbase
    print(f"Downloading cardbase @ [{download_uri}]")
    download_response = requests.get(download_uri)

    # Save the JSON response
    print(f"Saving file @ [{filename}]")
    with open(filename, "w") as file:
        json.dump(download_response.json(), file)
else:
    print("Skipping cardbase download (Set dl_cb to True to download the cardbase).")
    
# API endpoints for catalogs
catalog_type_uris = {
    "supertypes":"https://api.scryfall.com/catalog/supertypes", 
    "card_types":"https://api.scryfall.com/catalog/card-types", 
    "subtypes":{   
        "artifact_types":"https://api.scryfall.com/catalog/artifact-types",
        "battle_types":"https://api.scryfall.com/catalog/battle-types",
        "creature_types":"https://api.scryfall.com/catalog/creature-types",
        "enchantment_types":"https://api.scryfall.com/catalog/enchantment-types",
        "land_types":"https://api.scryfall.com/catalog/land-types",
        "planeswalker_types":"https://api.scryfall.com/catalog/planeswalker-types",
        "spell_types":"https://api.scryfall.com/catalog/spell-types"
    }
}

# Catalog filename
filename = "catalog.json"

# Create a dictionary to contain catalog data
catalog = {}

if dl_cl:
    # Add delay between requests to prevent excessive requests
    time.sleep(wait_time)

    # Function to make catalog fetches
    def catalog_fetch(dict: dict, name: str, wait_time: int = 1):
        uri = dict[name]
        print(f"Making {name} catalog request @ [{uri}]")
        time.sleep(wait_time)
        return list(requests.get(uri).json()["data"])

    # Get supertype catalog and card type catalog
    catalog["supertypes"] = catalog_fetch(catalog_type_uris, "supertypes", wait_time)
    catalog["card_types"] = catalog_fetch(catalog_type_uris, "card_types", wait_time)

    # Get subtype catalogs
    subtypes = []
    for subtype, uri in catalog_type_uris["subtypes"].items():
        subtypes += catalog_fetch(catalog_type_uris["subtypes"], subtype, wait_time)

    catalog["subtypes"] = subtypes

    with open(filename, "w") as file:
        json.dump(catalog, file)
else:
    print("Skipping catalog downloads (Set dl_cl to True to download the catalogs).")
