import os
from pathlib import Path
import json
import requests
from DataDragon import loader


moduleDir = os.path.dirname(os.path.abspath(__file__))
repoRoot = os.path.dirname(os.path.dirname(moduleDir))
MATCH_DIR = os.path.join(repoRoot, "data", "raw", "matches")
RUNES_PATH = os.path.join(repoRoot, "data", "runes.json")

def getRunesStat(files):
    count = {}
    for i in range(len(files)):
        try:
            with files[i].open(encoding="utf-8") as file:
                match = json.load(file)
        except json.JSONDecodeError:
            continue
        if match["info"]["gameDuration"] < 300:
            continue
        participants = match["info"]["participants"]
        for player in range(len(participants)):
            champion = participants[player]["championName"]
            role = participants[player]["teamPosition"]
            win = participants[player]["win"]

            keystone = participants[player]["perks"]["styles"][0]["selections"][0]["perk"]
            secRune = participants[player]["perks"]["styles"][1]["style"]
            key = (champion, role, keystone, secRune)
            if key not in count:
                count[key] = {"games": 0, "wins": 0}
            count[key]["games"] += 1
            if win:
                count[key]["wins"] += 1
    return count

def pickRunes(count, minGames):
    rune = {}
    keyList = list(count.keys())
    for i in range(len(keyList)):
        key = keyList[i]
        if count[key]["games"] < minGames:
            continue
        winrate = count[key]["wins"] / count[key]["games"]
        champLane = (key[0],key[1])
        if champLane not in rune:
            rune[champLane] = []
        rune[champLane].append((winrate, key[2],key[3]))

    finalRune = {}
    runeKey = list(rune.keys())
    for i in range(len(runeKey)):
        champLanes = runeKey[i]
        rune[champLanes].sort(reverse=True)
        best = rune[champLanes][0]
        finalRune[champLanes] = (best[1],best[2])
    return finalRune

def toJsonFormat(finalRune, patch):
    buildsFile = {}
    keyList = list(finalRune.keys())
    for i in range(len(keyList)):
        champName = keyList[i][0]
        lane = keyList[i][1]
        champDict = buildsFile.setdefault(champName, {})
        champDict[lane] = {"runes": finalRune[keyList[i]]}
    return {"patch": patch, "runes": buildsFile}

#Test 
if __name__ == "__main__":
    files = sorted(Path(MATCH_DIR).glob("*.json"))
    counts = getRunesStat(files)
    builds = pickRunes(counts, 30)
    print(len(builds))
    print(builds[("Riven", "TOP")])
    output = toJsonFormat(builds, loader.getVersionString())
    BUILD_PATH = os.path.join(repoRoot, "data", "runes.json")
    with open(BUILD_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)