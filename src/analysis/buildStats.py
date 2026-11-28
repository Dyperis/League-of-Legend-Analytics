import os
from pathlib import Path
import json
from DataDragon import filters, loader
import requests

moduleDir = os.path.dirname(os.path.abspath(__file__))
repoRoot = os.path.dirname(os.path.dirname(moduleDir))
MATCH_DIR = os.path.join(repoRoot, "data", "raw", "matches")
BUILD_PATH = os.path.join(repoRoot, "data", "builds.json")

#Count each items' win and game relative to champion and lane 
def countItemWinsStats(files):
    counts = {}
    for i in range(len(files)):
        try:
            with files[i].open(encoding="utf-8") as file:
                match = json.load(file)
        except json.JSONDecodeError:
            continue
        if match["info"]["gameDuration"] < 300: #Skip game that are remakes 
            continue
        participants = match["info"]["participants"]
        for player in range(len(participants)):
            champion = participants[player]["championName"]
            role = participants[player]["teamPosition"]
            win = participants[player]["win"]
            for itemCount in range(6):
                if participants[player][f"item{itemCount}"] == 0:
                    continue
                items = participants[player][f"item{itemCount}"]
                key = (champion, role, items)
                if key not in counts:
                    counts[key] = {"games": 0, "wins": 0}
                counts[key]["games"] += 1
                if win:
                    counts[key]["wins"] += 1
                
            
    return counts

#Find the best builds for each champions relative to lane. Low pickrate build get filtered
def pickBuilds(counts, minGames, catalog): 
    builds = {}
    keyList = list(counts.keys())
    for i in range(len(keyList)):
        key = keyList[i]
        if counts[key]["games"] < minGames:
            continue
        if filters.isCompleteItem(key[2], catalog) == False:
            continue

        winrate = counts[key]["wins"] / counts[key]["games"]
        champLane = (key[0],key[1])
        if champLane not in builds:
            builds[champLane] = []
        builds[champLane].append((winrate, key[2]))

    finalBuilds = {}
    buildKey = list(builds.keys())
    for i in range(len(buildKey)):
        champLanes = buildKey[i]
        builds[champLanes].sort(reverse=True)
        top6 = builds[champLanes][:6]
        finalBuilds[champLanes] = []
        for j in range(len(top6)):
            finalBuilds[champLanes].append(top6[j][1])
    return finalBuilds

#Turn pickBuilds() result into a JSON file so it can be used for the app
def toJsonFormat(finalBuilds, patch):
    buildsFile = {}
    keyList = list(finalBuilds.keys())
    for i in range(len(keyList)):
        champName = keyList[i][0]
        lane = keyList[i][1]
        champDict = buildsFile.setdefault(champName, {})
        champDict[lane] = {"items": finalBuilds[keyList[i]]}
    return {"patch": patch, "builds": buildsFile}

    
#Test and JSON file creation
if __name__ == "__main__":
    files = sorted(Path(MATCH_DIR).glob("*.json"))
    url = f"https://ddragon.leagueoflegends.com/cdn/{loader.getVersionString()}/data/en_US/item.json"
    response = requests.get(url)
    catalog = response.json()
    counts = countItemWinsStats(files)
    builds = pickBuilds(counts, 30, catalog)
    output = toJsonFormat(builds, loader.getVersionString())
    with open(BUILD_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

