# This file will contain all the functions that get the session data that we will analyze.
from typing import Optional, List, Dict
import requests

API = "https://api.openf1.org/v1"

_SessionAliases = {
    "race" : "Race",
    "sprint" : "Sprint",
    "quali": "Qualifying",
    "qualifying" : "Qualifying",
    "sprint quali" : "Sprint Qualifying",
    "sprint qualifying" : "Sprint Qualifying"
}

#Adding Alias variants for free practice.
for n in {1, 2, 3}:
    _SessionAliases[f"fp{n}"] = f"Practice {n}"
    _SessionAliases[f"free practice {n}"] = f"Practice {n}"
    _SessionAliases[f"freepractice{n}"] = f"Practice {n}"

'''Normalizes session name input to ensure it is a valid input.
If input is None, use None. If input is in _SessionAlias, use the corresponding Value.
IF input not None and not in _SessionAlias, raise ValueError'''
def normalizeSessionName(name: Optional[str]) -> Optional[str]:
    if name is None:
        return None
    key = str(name).strip().lower()

    if key in _SessionAliases:
        return _SessionAliases[key]
    raise ValueError(f"Unknown Session Name [{name}]. Valid options: {list(_SessionAliases.keys())}")

'''Returns all {sessionName} sessions for the year.
Each {sessionName} item contains session_key, location, session_name, date.'''
def fetchSessions(year: int, session_name: Optional[str] = None) -> List[Dict]:
    url = f"{API}/sessions"
    params = {"year":year}
    try:
        normalizedName = normalizeSessionName(session_name)
    except ValueError as e:
        print(str(e))
        quit(1)

    params["session_name"] = normalizedName

    response = requests.get(url,params=params,timeout=30)
    response.raise_for_status()

    return response.json()

'''Helper function to fetch session data using its session_key'''
def fetchSessionByKey(session_key: int or str) -> Dict:
    url = f"{API}/sessions"
    params = {"session_key":session_key}
    response = requests.get(url,params,timeout=30)
    response.raise_for_status()
    data = response.json()

    if not data:
        raise ValueError(f"No session data found for session_key = {session_key}")
    return data[0]

'''Helper function to find session data by either location or name'''
def fetchSessionsByName(year: int, name_substring:str, session_name: Optional[str] = None) -> List[Dict]:
    all_sessions = fetchSessions(year,session_name)
    substring_lower = name_substring.strip().lower()

    matching_sessions = []

    for s in all_sessions:
        location = s.get("location","").lower()
        country = s.get("country_name","").lower()
        name = s.get("name","").lower()

        if (substring_lower in location
            or substring_lower in name
                or substring_lower in country):
            matching_sessions.append(s)

    return matching_sessions

'''Helper function to fetch the latest session'''
def fetchLatestSession() -> Dict:
    return fetchSessionByKey("latest")

'''Simple helper function to print out the desired sessions in the entire year.'''
def printSessionList(year: int, session_name: Optional[str] = None) -> None:
    sessions = fetchSessions(year,session_name)
    label = session_name or "ALL"
    print(f"Sessions for {year} ({label}):")
    for s in sessions:
        key = s.get("session_key")
        country_name = s.get("country_name")
        location = s.get("location", s.get("name","Unknown"))
        start = s.get("date_start", s.get("date", "No date known"))

        print(f"{key} – {country_name} – {location} ({start})")

'''Helper to print details of a given dictionary in readable format'''
def printSessions(sessions: List[Dict] or Dict) -> None:
    if not sessions:
        print("No Sessions Found.")
        return
    if type(sessions) == dict:
        sessions = [sessions]
    for s in sessions:
        key = s.get("session_key")
        country_name = s.get("country_name")
        location = s.get("location", s.get("name", "Unknown"))
        session_name = s.get("session_name")
        start = s.get("date_start", s.get("date", "No date known"))

        print(f"{key} – {country_name} – {location} – {session_name} – ({start})")