import os
import time
import requests
from dotenv import load_dotenv

load_dotenv(override=True) 
api_key = os.getenv("RIOT_API_KEY")
if api_key is None:
        raise Exception("Error: RIOT_API_KEY does not exist")

#Send a request to riot games using the Developer API
def riotGet(url, params=None):
    time.sleep(1.2)    
    headers = {"X-Riot-Token": api_key}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.RequestException as e:
        print("Error " + str(e))
        return None
    
    if response.status_code == 200: #Correct behavior
        return response.json()
    elif response.status_code == 429: #Over rate limit
        retry_after = int(response.headers.get("Retry-After", 1))
        time.sleep(retry_after)
        return riotGet(url, params)
    elif response.status_code == 404: #If riot server is down
        return None
    elif response.status_code == 403 or response.status_code == 401: #Problems w api keys
        raise Exception(f"Error: {response.status_code} - {response.text}. API key expired.")
    else:
        print(f"Error: {response.status_code} - {url}")
        return None
