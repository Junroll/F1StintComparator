from typing import Optional
from data_fetching import fetch_stints as fS, fetch_laps as fL

'''Creates a dictionary for each driver based on their driver number
and fills out the following information according to their stint informations
- "compounds" -> array containing the order of the tires in the race
- "laptimes" -> array of arrays, with each interior arrays being laptimes of the corresponding stints
- "pit_out_lap" -> arrray containing the laps where the driver exited the pits.
The dictionary for each driver is nested into a parent dictionary, where the driver_number is the key.'''
def sortDriverLaps(session_key: int, driver_number: Optional[int] = None) -> dict:
    stints = fS.fetchStints(session_key, driver_number)
    driverLapData = {}

    for s in stints:
        driver = s.get("driver_number")
        if driver not in driverLapData.keys():
            driverLapData[driver] = {
                "compounds": [],
                "laptimes": [],
                "pit_out_lap": []
            }
        driverData = driverLapData[driver]
        index = s.get("stint_number") - 1
        stintLapTimes = []
        segmentLaps = fL.fetchLapsBySegment(session_key, s["lap_start"], s["lap_end"], driver)
        for lap in segmentLaps:
            if lap["lap_duration"] is None:
                stintLapTimes.append(0)
            else: stintLapTimes.append(lap["lap_duration"])

            if lap["is_pit_out_lap"]:
                driverData["pit_out_lap"].append(lap["lap_number"])

        driverData["compounds"].insert(index, s["compound"])
        driverData["laptimes"].insert(index, stintLapTimes)

    return driverLapData

'''Helper function to print the data obtained by the above function.'''
def printLaptimeInformation(driverLapData: dict) -> None:
   if not driverLapData:
       print("No driver lap data.")
       return

   for driver in driverLapData.keys():
    driverData = driverLapData.get(driver)

    for index in range(len(driverData.get("compounds"))):
        print(f"Driver {driver} – {driverData.get("compounds")[index]} – {driverData.get("laptimes")[index]}")
    print(f"Pit Out Laps – {driverData.get("pit_out_lap")}")
    print("-"*40)