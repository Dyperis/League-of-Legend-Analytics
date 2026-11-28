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

