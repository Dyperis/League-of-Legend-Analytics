from DataDragon import loader
import requests
version = loader.getVersionString()

champUrl = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
champResponse = requests.get(champUrl)
champCatalog = champResponse.json()

itemUrl = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
itemResponse = requests.get(itemUrl)
itemCatalog = itemResponse.json()

runeUrl = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
runeResponse = requests.get(runeUrl)
runeCatalog = runeResponse.json()
runeNames = {}

for tree in runeCatalog:
    runeNames[tree["id"]] = tree["name"]  # Store the tree itself

    for slot in tree["slots"]:
        for rune in slot["runes"]:
            runeNames[rune["id"]] = rune["name"]

#Find Champion Name
def findChampion(champId):
    result = champCatalog["data"].get(champId)
    if result is None:
        return champId
    return result["name"]

#Find Item Name
def findItem(itemId):
    result = itemCatalog["data"].get(str(itemId))
    if result is None:
        return str(itemId)
    return result["name"]

#Find Rune Name
def findRune(runeId):
    return runeNames.get(runeId, str(runeId))


if __name__ == "__main__":
    print(findChampion("MonkeyKing"), findItem(6694), findRune(8010), findRune(8400))

#Legacy code. I thought i would need this when I started but then decided not to use them
#They will however still be saved because I might need them in the future
"""
def simplify(name):
    return name.lower().replace(" ", "").replace(",", "").replace("'", "").replace(".", "").replace("&", "").replace(":", "")

def lookUpChampion(championName):
    url = f"https://ddragon.leagueoflegends.com/cdn/{loader.getVersionString()}/data/en_US/champion.json"
    response = requests.get(url)
    name = simplify(championName)
    catalog = response.json()
    for champion in catalog["data"].values():
        if simplify(champion["name"]) == name:
            return champion["key"]

def lookUpItem(itemName):
    url = f"https://ddragon.leagueoflegends.com/cdn/{loader.getVersionString()}/data/en_US/item.json"
    response = requests.get(url)
    name = simplify(itemName)
    catalog = response.json()
    for item_id, item in catalog["data"].items():
        if simplify(item["name"]) == name:
            if filters.isBuildable(item_id, catalog):
                return item_id

def lookUpRunes(runesName):
    url = f"https://ddragon.leagueoflegends.com/cdn/{loader.getVersionString()}/data/en_US/runesReforged.json"
    response = requests.get(url)
    name = simplify(runesName)
    catalog = response.json()
    for path in catalog:
        for slot in path["slots"]:
            for rune in slot["runes"]:
                if simplify(rune["name"]) == name:
                    return rune["id"]
"""