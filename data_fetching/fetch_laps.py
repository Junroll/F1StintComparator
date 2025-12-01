from typing import Optional, List, Dict
import requests

API = "https://api.openf1.org/v1"

'''Fetches lap data for a given {session_key}, with optional filtering
Returns a list of dicts where each dict include keys like:
- driver_number
- lap_number
- lap_duration
- is_pit
- sectors
and more
'''
def fetchLaps(session_key: int,
              driver_number: Optional[int] = None,
              lap_number: Optional[int] = None) -> List[Dict]:
    url = f"{API}/laps"
    params = {"session_key": session_key}

    #Optional Filters
    if driver_number is not None:
        params["driver_number"] = driver_number
    if lap_number is not None:
        params["lap_number"] = lap_number

    response = requests.get(url,params=params,timeout=30)
    response.raise_for_status()

    return response.json()

'''Helper method to fetch laps by driver'''
def fetchLapsByDriver(session_key: int, driver_number: int) -> List[Dict]:
    return fetchLaps(session_key,driver_number)

'''Helper method to fetch laps by Lap Segments with optional driver filtering'''
def fetchLapsBySegment(session_key: int,
                       lap_start: int,
                       lap_end: int,
                       driver_number: Optional[int] = None) -> List[Dict]:
    if lap_start is None or lap_end is None or lap_start > lap_end:
        raise ValueError("Invalid lap_start/lap_end. Require lap_start <= lap_end.")

    all_Laps = fetchLaps(session_key, driver_number)
    segment = []

    for lap in all_Laps:
        lap_number = lap.get("lap_number")
        if lap_number is None:
            continue
        if lap_number > lap_end:
            break
        if lap_start <= lap_number <= lap_end:
            segment.append(lap)

    return segment


'''Helper method to print lap data in human readable format'''
def printLaps(laps: List[Dict]) -> None:
    if not laps:
        print("No laps found.")
        return

    for lap in laps:
        print(
            f"Driver {lap['driver_number']} | Lap {lap['lap_number']} | "
            f"Time {lap.get('lap_duration', 'N/A')} | Out Lap {lap.get('is_pit_out_lap', 'N/A')}"
        )