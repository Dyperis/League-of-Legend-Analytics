from collector import riotClient
import os
import json
from datetime import datetime, timezone

START_TIME = int(datetime(2026, 11, 4, tzinfo=timezone.utc).timestamp())   # patch 26.22
END_TIME   = int(datetime(2026, 11, 18, tzinfo=timezone.utc).timestamp())  # patch 26.23

PLATFORM_URL = "https://na1.api.riotgames.com"
REGION_URL = "https://americas.api.riotgames.com"

def getHighEloPuuids(): # Get the elo of top players in the region
    resultlist = []
    challenger = riotClient.riotGet(f"{PLATFORM_URL}/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5")
    if challenger is not None:
        for entry in challenger["entries"]:
            resultlist.append(entry["puuid"])

    grandmaster = riotClient.riotGet(f"{PLATFORM_URL}/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5")
    if grandmaster is not None:
        for entry in grandmaster["entries"]:
            resultlist.append(entry["puuid"])

    master = riotClient.riotGet(f"{PLATFORM_URL}/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5")
    if master is not None:
        for entry in master["entries"]:
            resultlist.append(entry["puuid"])
    return resultlist

def getMatchID(puuid, startTime, endTime): #Get match ID from top players
    params = {"startTime": startTime, "endTime": endTime, "queue": 420, "count": 100}
    url = f"{REGION_URL}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    matchID = riotClient.riotGet(url, params=params)
    if matchID is None:
        print(f"No matches found")
        matchID = []
    return matchID

moduleDir = os.path.dirname(os.path.abspath(__file__))
repoRoot = os.path.dirname(os.path.dirname(moduleDir))
MATCH_DIR = os.path.join(repoRoot, "data", "raw", "matches")
MATCH_IDS_PATH = os.path.join(os.path.dirname(MATCH_DIR), "matchIds.json")

def saveMatch(matchId): #Save each match as JSON file to be used
    path = os.path.join(MATCH_DIR, f"{matchId}.json")
    if os.path.isfile(path):
        return False
    match = riotClient.riotGet(f"{REGION_URL}/lol/match/v5/matches/{matchId}")
    if match is None:
        return False

    os.makedirs(MATCH_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(match, file)
    return True


if __name__ == "__main__":
    if os.path.isfile(MATCH_IDS_PATH):
        with open(MATCH_IDS_PATH, "r", encoding="utf-8") as file:
            matchList = json.load(file)
        print(f"Loaded {len(matchList)} match IDs from cache")
    else:
        puuids = getHighEloPuuids()
        print(f"Found {len(puuids)} players")

        matchIds = set()
        for i in range(len(puuids)):
            ids = getMatchID(puuids[i], START_TIME, END_TIME)
            matchIds.update(ids)

            done = i + 1
            if done % 25 == 0 or done == len(puuids):
                print(f"{done}/{len(puuids)} players checked, {len(matchIds)} unique IDs")

        matchList = sorted(matchIds)
        os.makedirs(os.path.dirname(MATCH_IDS_PATH), exist_ok=True)

        tempPath = MATCH_IDS_PATH + ".tmp"
        with open(tempPath, "w", encoding="utf-8") as file:
            json.dump(matchList, file)
        os.replace(tempPath, MATCH_IDS_PATH)
        print(f"Cached {len(matchList)} match IDs")

    saved = 0
    for i in range(len(matchList)):
        if saveMatch(matchList[i]):
            saved += 1

        done = i + 1
        if done % 50 == 0 or done == len(matchList):
            print(f"{done}/{len(matchList)} matches checked, {saved} new files saved")

    print(f"Done: saved {saved} new matches out of {len(matchList)} IDs")