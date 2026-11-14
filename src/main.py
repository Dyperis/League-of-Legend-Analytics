import json
import requests
from DataDragon import loader

catalog = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{loader.getVersionString()}/data/en_US/item.json").json()
print(len(catalog["data"]))

for item_id, item in catalog["data"].items():
    if "requiredAlly" in item:
        print(item_id, item["name"])

