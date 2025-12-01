from typing import Optional
from data_fetching import fetch_stints as fS, fetch_laps as fL

'''Creates a dictionary for each driver based on their driver number
and fills out the following information according to their stint informations
- "compounds" -> array containing the order of the tires in the race
- "laptimes" -> array of arrays, with each interior arrays being laptimes of the corresponding stints
- "pit_out_lap" -> arrray containing the laps where the driver exited the pits.
The dictionary for each driver is nested into a parent dictionary, where the driver_number is the key.'''
def sortDriverLaps(session_key: int,driver_number: Optional[int] = None) -> dict:
    stints = fS.fetchStints(session_key,driver_number)
    all_laps = fL.fetchLaps(session_key,driver_number)
    laps_by_driver = {}
    driverLapData = {}

    for lap in all_laps:
        driver = lap.get("driver_number")
        laps_by_driver.setdefault(driver,[]).append(lap)

    for s in stints:
        driver = s.get("driver_number")
        driverLapData.setdefault(driver,{
            "compounds": [],
            "laptimes": [],
            "pit_out_lap": []
        })
        driverData = driverLapData[driver]
        lap_start = s.get("lap_start")
        lap_end = s.get("lap_end")
        compound = s.get("compound")
        index = s.get("stint_number") - 1
        stintLapTimes = []

        if driver in laps_by_driver and lap_start is not None and lap_end is not None:
            segment = laps_by_driver[driver][lap_start-1:lap_end]

            for lap in segment:
                laptime = lap.get("lap_duration")
                stintLapTimes.append(laptime if laptime is not None else 0)
                if lap.get("is_pit_out_lap"):
                    driverData["pit_out_lap"].append(lap.get("lap_number"))
        else:
            stintLapTimes = []

        driverData["compounds"].insert(index,compound)
        driverData["laptimes"].insert(index,stintLapTimes)

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

printLaptimeInformation(sortDriverLaps(9850))