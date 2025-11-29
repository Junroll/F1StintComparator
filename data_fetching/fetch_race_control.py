from typing import Optional, List, Dict
import requests

API = "https://api.openf1.org/v1"

'''Fetches race control events, with the optional filter of choosing specific events'''
def fetchRaceEvents(session_key: int, category: Optional[str] = None, flag: Optional[str] = None) -> List[Dict]:
    url = f"{API}/race_control"
    params = {"session_key": session_key}

    if category is not None:
        params["category"] = category
    if flag is not None:
        params["flag"] = flag.upper()

    response = requests.get(url, params=params,timeout=30)
    response.raise_for_status()

    return response.json()

'''Helper to fetch Safety Car and VSC event data.'''
def fetchSafetyCar(session_key: int) -> List[Dict]:
    return fetchRaceEvents(session_key,category="SafetyCar")

'''Helper to fetch Yellow Flag event data'''
def fetchAllYellowFlags(session_key: int) -> List[Dict]:
    singleYellow = fetchRaceEvents(session_key,category="Flag",flag="YELLOW")
    doubleYellow = fetchRaceEvents(session_key,category="Flag",flag="DOUBLE YELLOW")

    return singleYellow+doubleYellow

'''Helper to getch Red Flag Event Data'''
def fetchRedFlags(session_key: int) -> List[Dict]:
    return fetchRaceEvents(session_key,category="Flag",flag="RED")

'''Helper to combine all helpers and create a pace impacting race events dictionary'''
def fetchPaceImpactEvents(session_key:int) -> List[Dict]:
    #Get individual events
    safetyCar = fetchSafetyCar(session_key)
    yellowFlags = fetchAllYellowFlags(session_key)
    redFlags = fetchRedFlags(session_key)

    #Ensure none of them is None as None does not have .append()
    if safetyCar is None: safetyCar = []
    if yellowFlags is None: yellowFlags = []
    if redFlags is None: redFlags = []

    #Merge the events for readability
    allEvents = safetyCar+yellowFlags+redFlags

    return allEvents

'''Helper to print event data in human readable format'''
def printRaceEvents(events: List[Dict]) -> None:
    if not events:
        print("No race events found.")
        return

    for ev in events:
        category = ev.get("category")
        lap = ev.get("lap_number")
        if category == "Flag": flag = ev.get("flag")
        else: flag = "Not Flag Event"
        message = ev.get("message")

        print(f"Lap {lap} – {category} – {flag} – {message}")


'''Function to create an array of laps that had an event'''
def lapsWithPaceEvents(session_key) -> List:
    events = fetchPaceImpactEvents(session_key)
    safetyCarEnding = False
    safetyCarDeployedLap = 0
    lapsAffected = []

    for ev in events:
        lap = ev.get("lap_number")
        category = ev.get("category")
        message = ev.get("message")

        if category == "SafetyCar" and "DEPLOYED" in message:
            safetyCarDeployedLap = lap
        elif category == "SafetyCar" and ("ENDING" in message or "IN THIS LAP" in message):
            safetyCarEnding = True

        if lap not in lapsAffected and safetyCarEnding:
            for lapNum in range(safetyCarDeployedLap,lap+1):
                if lapNum not in lapsAffected:
                    lapsAffected.append(lapNum)
            safetyCarEnding = False
        elif lap not in lapsAffected:
            lapsAffected.append(lap)

    return sorted(lapsAffected)