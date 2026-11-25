import os
from pathlib import Path
import json

moduleDir = os.path.dirname(os.path.abspath(__file__))
repoRoot = os.path.dirname(os.path.dirname(moduleDir))
RUNES_PATH = os.path.join(repoRoot, "data", "runes.json")
BUILD_PATH = os.path.join(repoRoot, "data", "builds.json")

with open(RUNES_PATH, encoding="utf-8") as f:
    runes = json.load(f)
with open(BUILD_PATH, encoding="utf-8") as f:
    item = json.load(f)

def recommend(champ, lane):
    if champ in item["builds"] and champ in runes["runes"]:
        if lane in item["builds"][champ] and lane in runes["runes"][champ]:
            return (item["builds"][champ][lane]["items"],runes["runes"][champ][lane]["runes"])

    return None



if __name__ == "__main__":
    print(recommend("Riven", "TOP"))
    print(recommend("Riven", "UTILITY"))