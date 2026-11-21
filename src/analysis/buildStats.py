import os
from pathlib import Path
import json

moduleDir = os.path.dirname(os.path.abspath(__file__))
repoRoot = os.path.dirname(os.path.dirname(moduleDir))
MATCH_DIR = os.path.join(repoRoot, "data", "raw", "matches")
MATCH_IDS_PATH = os.path.join(os.path.dirname(MATCH_DIR), "matchIds.json")

def countItemWinsStats(files):
    counts = {}
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

#Test
if __name__ == "__main__":
    files = sorted(Path(MATCH_DIR).glob("*.json"))
    counts = countItemWinsStats(files[:100])
    print(len(counts))
    keys = list(counts.keys())
    for i in range(5):
        print(keys[i], counts[keys[i]])