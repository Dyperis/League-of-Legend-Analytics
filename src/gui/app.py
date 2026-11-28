import os
from pathlib import Path
import json
import customtkinter as ctk
from DataDragon import lookups
from difflib import get_close_matches

moduleDir = os.path.dirname(os.path.abspath(__file__))
repoRoot = os.path.dirname(os.path.dirname(moduleDir))
RUNES_PATH = os.path.join(repoRoot, "data", "runes.json")
BUILD_PATH = os.path.join(repoRoot, "data", "builds.json")

with open(RUNES_PATH, encoding="utf-8") as f:
    runes = json.load(f)
with open(BUILD_PATH, encoding="utf-8") as f:
    item = json.load(f)

#function to get data to UI
def recommend(champ, lane):
    if champ in item["builds"] and champ in runes["runes"]:
        if lane in item["builds"][champ] and lane in runes["runes"][champ]:
            return (item["builds"][champ][lane]["items"],runes["runes"][champ][lane]["runes"])

    return None



#Change name in display for easier use
LANE_LABELS = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Mid", "BOTTOM": "ADC", "UTILITY": "Support"}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("League of Legends Analytics")
        self.geometry("800x500")

        self.selectedChamp = None
        self.selectedLane = None

        self.nameToId = {}
        champIds = list(item["builds"].keys())
        for i in range(len(champIds)):
            displayName = lookups.findChampion(champIds[i])
            self.nameToId[displayName] = champIds[i]
        self.champNames = sorted(self.nameToId.keys())
        self.champBox = ctk.CTkComboBox(self, values=self.champNames, command=self.onChampSelect)
        self.champBox.set("")
        self.champBox.bind("<KeyRelease>", self.searchChamps)
        self.laneButtons = ctk.CTkSegmentedButton(self, values=list(LANE_LABELS.values()),command=self.onLaneSelect)
        self.resultsLabel = ctk.CTkLabel(self, text="Pick a champion and lane",justify="left")
        self.champBox.pack(pady=10)
        self.laneButtons.pack(pady=10)
        self.resultsLabel.pack(pady=10)

    def searchChamps(self, event):
        query = self.champBox.get().strip().title()
        if query:
            matches = get_close_matches(query, self.champNames, n=5, cutoff=0.2)
            self.champBox.configure(values=matches)
        else:
            self.champBox.configure(values=self.champNames)

    def onChampSelect(self, displayName):
        self.selectedChamp = self.nameToId[displayName]
        self.showResults()

    def onLaneSelect(self, lane):
        for key, label in LANE_LABELS.items():
            if (label == lane): 
                self.selectedLane = key
                self.showResults()
                break
        
    def showResults(self):
        if self.selectedChamp is None or self.selectedLane is None:
            return

        result = recommend(self.selectedChamp, self.selectedLane)
        if result is None:
            self.resultsLabel.configure(text="No data for this champion/lane")
            return
        items, runeData = result
        lines = [
            f"Keystone: {lookups.findRune(runeData[0])}",
            f"Secondary: {lookups.findRune(runeData[1])}",
            "",
            "Items:"
        ]

        for i in range(len(items)):
            itemName = lookups.findItem(items[i])
            lines.append(f"{i + 1}. {itemName}")

        self.resultsLabel.configure(text="\n".join(lines))
        

