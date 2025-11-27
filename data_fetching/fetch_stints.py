from typing import Optional,List, Dict
import requests

API = "https://api.openf1.org/v1"

'''Function returns the stints of a given race determined by the {session_key} and oher optional parameters
Returns a list of dicts where each dict contains:
- driver_number
- compound
- lap_start
- lap_end
- (more info not currently required)
Raises ValueError if compound input is not in the tire_compounds list.
'''
def fetchStints(session_key: int,
                driver_number: Optional[int] = None,
                stint_number: Optional[int] = None,
                compound: Optional[str] = None) -> List[Dict]:
    tire_compounds = ["SOFT","MEDIUM","HARD","INTERMEDIATE","WET"]

    url = f"{API}/stints"
    params = {"session_key": session_key}

    if driver_number is not None:
        params["driver_number"] = driver_number
    if stint_number is not None:
        params["stint_number"] = stint_number
    if compound is not None:
        if compound.upper() not in tire_compounds:
            raise ValueError(f"Invalid compound: {compound}. Must be one of {tire_compounds}")
        params["compound"] = compound

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()

'''Helper function that utilizes the main function to filter by driver_number'''
def fetchStintsByDriver(session_key: int, driver_number: int) -> List[Dict]:
    return fetchStints(session_key,driver_number)

'''Helper function that utilizes the main function to filter by stint_number'''
def fetchStintsByNumber(session_key: int,stint_number: int) -> List[Dict]:
    return fetchStints(session_key,stint_number=stint_number)

'''Helper function that utlizes the main function to filter by compound'''
def fetchStintsByCompound(session_key: int,compound: str) -> List[Dict]:
    return fetchStints(session_key,compound=compound)

'''Simple helper functions to cleanly print stint information'''
def printStints(stints: List[Dict]) -> None:
    if not stints:
        print("No stints found")
        return

    for s in stints:
        print(
            f"Driver {s['driver_number']} | Stint {s['stint_number']} | "
            f"Laps {s['lap_start']}-{s['lap_end']} | Tyre {s['compound']} "
            f"(age {s['tyre_age_at_start']})"
        )