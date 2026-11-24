import json
import requests
from DataDragon import loader, lookups
from collector import riotClient

result =riotClient.riotGet("https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5", params=None)
print(type(result))
print(result.keys())
print(len(result["entries"]))
print(result["entries"][0])
print(lookups.lookUpItem(2517))
