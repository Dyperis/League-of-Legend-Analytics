import loader
import requests

def simplify(name):
    return name.lower().replace(" ", "").replace(",", "").replace("'", "").replace(".", "").replace("&", "").replace(":", "")

def lookUpChampion(championName):
    url = f"https://ddragon.leagueoflegends.com/cdn/{loader.get_version_string()}/data/en_US/champion.json"
    response = requests.get(url)
    name = simplify(championName)
    catalog = response.json()
    for champion in catalog["data"].values():
        if simplify(champion["name"]) == name:
            return champion["key"]

    
def lookUpItem(itemName):
    url = f"https://ddragon.leagueoflegends.com/cdn/{loader.get_version_string()}/data/en_US/item.json"
    response = requests.get(url)
    name = simplify(itemName)
    catalog = response.json()
    for item_id, item in catalog["data"].items():
        if simplify(item["name"]) == name:
            return item_id

def lookUpRunes(runesName):
    url = f"https://ddragon.leagueoflegends.com/cdn/{loader.get_version_string()}/data/en_US/runesReforged.json"
    response = requests.get(url)
    name = simplify(runesName)
    catalog = response.json()
    for path in catalog:
        for slot in path["slots"]:
            for rune in slot["runes"]:
                if simplify(rune["name"]) == name:
                    return rune["id"]