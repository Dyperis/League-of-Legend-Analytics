#This part get the latest version of league.
import requests
def getVersionString():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    versionArray = requests.get(url).json()
    version_string = versionArray[0]
    return version_string

#Might add caching and timeout errors in the future