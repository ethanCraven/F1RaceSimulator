



import os
import csv
import pandas as pd
import constants
import driver
import importlib
import Track_sectors
import random
import math
from collections import OrderedDict
import ast
import sys




importlib.reload(driver)
importlib.reload(constants)
importlib.reload(Track_sectors)
from driver import Driver
from constants import DB_DRIVER_NAMES, DEFAULT_BASE_LAP, DRIVER_CONSTANTS, PREV_RACE_RESULTS, AVG_PIT_LOSS, NUMBER_OF_LAPS
from Track_sectors import TRACK_SECTORS

def resource_path(relative_path):

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



quali_df = pd.read_csv(resource_path('Data/all_quali_data.csv'))
race_df = pd.read_csv(resource_path('Data/all_race_data.csv'))
compounds = ["soft", "medium", "hard"]





#This method returns the average pitstop loss for a given race. At the moment it is just the Dutch GP
#More will be added later
def get_avg_pit_loss(race):
    avg_pit_loss = AVG_PIT_LOSS[race]
    return float(avg_pit_loss)





def find_driver_list(race):
    driver_list = []
    for driver_name in DB_DRIVER_NAMES:
        if driver_name in PREV_RACE_RESULTS[race]:
            driver_list.append(driver_name)
    return driver_list





def get_base_time(race, year, driver):
    base_time = (quali_df[(quali_df.year == year) & (quali_df.race_name == f"{race}") & (quali_df.driver == f"{driver}")])
    if base_time.empty:
        return DEFAULT_BASE_LAP[f"{race}"]
    return float(base_time.iloc[0, 3])



def get_number_of_laps(race):
    return NUMBER_OF_LAPS[race]




#Calculates the next compound the driver should be on.
def get_next_compound(current_compound):
    if current_compound == "soft":
        return compounds[random.randint(1,2)]
    elif current_compound == "medium":
        return compounds[random.randint(0,2)]
    else:
        return compounds[random.randint(0,1)]



def simulate_sector_times(driver, race):
    lap_time, sector_times = driver.simulate_sector_times(driver.stint_lap, race)
    return lap_time, sector_times





def is_DRS_available(gap_to_in_front, lap):
    if lap > 3 and gap_to_in_front < 1.0:
        return True
    else:
        return False





#calculates DRS effect using the speed increase in m/s. 
def get_DRS_affect(race, sector_number, sector_time):
    speed_increase = 3.6
    sector = TRACK_SECTORS[race][sector_number]
    distance = sector['end'] - sector['start']
    original_speed = distance / sector_time
    drs_speed = original_speed + speed_increase
    new_sector_time = distance / drs_speed
    return new_sector_time



#Calculates the sector difference when gaining speed due to slipstream. 
def get_slipstream_affect(race, sector_number, sector_time, interval):
    sector = TRACK_SECTORS[race][sector_number]
    sector_distance = sector["end"] - sector["start"]
    if 0 < interval < 1.2:
        time_gain = (-0.24 * interval + 0.3) * (sector_distance / 750)
        return sector_time - time_gain
    else:
        return sector_time



#Calculates the turbulence effect from following another car. 
def get_following_cornering_affect(race, sector_number, sector_time, interval):
    if interval < 0 or interval > 3:
        return sector_time
    sector = TRACK_SECTORS[race][sector_number]
    b = 0.0015
    sector_speed = sector["speed"]
    sector_distance = sector["end"] - sector["start"]
    gap_effect = (1 / (interval + 0.0001))
    if sector_speed == "fast":
        sector_speed_effect = 0.25
    elif sector_speed == "medium":
        sector_speed_effect = 0.15
    else:
        sector_speed_effect = 0.1 
    sector_distance_effect = math.log(b * sector_distance + 1)
    time_loss = gap_effect * sector_speed_effect * sector_distance_effect
    if time_loss > 0.6:
        time_loss = 0.6
    sector_time = float(sector_time) + time_loss
    return sector_time










def increment_laps(drivers):
    for driver in drivers:
        driver.current_lap += 1
        driver.stint_lap += 1





def order_drivers_by_race_time(drivers):
    drivers.sort(key=lambda d: d.race_time)
    for idx, driver in enumerate(drivers):
        driver.position = idx + 1
    return drivers





def order_drivers_by_position(drivers):
    drivers.sort(key=lambda d: d.position)
    for idx, driver in enumerate(drivers):
        driver.position = idx + 1
    return drivers




def calculate_gaps_to_in_front(drivers):
    for i in range(1, len(drivers)):
        interval = drivers[i].race_time - drivers[i-1].race_time
        drivers[i].gap_to_in_front = interval




def get_tyre_traction_level(compound):
    if compound == "soft":
        return 1.0
    elif compound == "medium":
        return 0.9
    else:
        return 0.8



#Method that calculates the initial sector of a race
def calculate_starting_sector(driver):
    base_acceleration = 10.31630769 
    #The Drivers starting skill rating
    driver_skill = DRIVER_CONSTANTS[driver.driver_id]['starting']
    if (random.uniform(0, 1.05) > driver_skill):
        #Driver has performed a bad start
        random_multiplier = random.uniform(0.95, 0.99)
        base_acceleration *= random_multiplier
    tyre_traction = get_tyre_traction_level(driver.compound)
    varied_acceleration = base_acceleration * tyre_traction
    sector_time = (((driver.starting_distance * 2)/ varied_acceleration) ** 0.5)
    return sector_time





def use_best_strategy(best_strategy_dictionary, driver):
    starting_tyre = list(best_strategy_dictionary[driver].keys())[0][0]
    suggested_strategy = list(best_strategy_dictionary[driver].keys())[0]
    return starting_tyre, suggested_strategy




#Initialises all the drivers and their starting variable values. 
def initialise_starting_variables(race, year, best_strategy):
    driver_list = find_driver_list(race)
    drivers = []
    compounds = ["soft", "medium", "hard"]
    for driver_name in driver_list:
        if best_strategy == None:
            starting_compound = compounds[random.randint(0,2)]
            suggested_strategy = None
        else:
            starting_compound, suggested_strategy = use_best_strategy(best_strategy, driver_name)

        drivers.append(Driver(driver_id=driver_name, base_lap_time=get_base_time(race, year, driver_name),
                                fuel_level=110, starting_compound=starting_compound,
                                race_name = race, expected_strategy=suggested_strategy))
    drivers.sort(key= lambda d: d.base_lap_time)
    for idx, driver in enumerate(drivers):
        driver.position = idx + 1
        driver.grid_slot = driver.position
        driver.starting_distance = driver.get_starting_distance(race)
        driver.starting_sector = calculate_starting_sector(driver)
        driver.compounds.append(driver.starting_compound)
    number_of_sectors = len(TRACK_SECTORS[race])
    return drivers, number_of_sectors





def get_overtake_probability(race, sector_number, driver1, driver2):
    sector_probability = TRACK_SECTORS[race][sector_number]["overtake_probability"]
    #Interval is how much ahead the driver is going to be
    interval = driver2.race_time - driver1.race_time
    interval_factor = min(interval / 0.4, 1)
    overtake_probability = sector_probability * interval_factor
    return overtake_probability   



#Calculates any overtakes that will occur during the sector. 
def calculate_overtakes(drivers, race, sector_number):
    for i in range(len(drivers) - 1, 0, -1):
        driver = drivers[i]
        if driver.position > 1:
            while driver.position > 1:
                driver_in_front = drivers[i - 1]
                if driver.race_time < driver_in_front.race_time:
                    overtaking_probability = get_overtake_probability(race, sector_number, driver, driver_in_front)
                    if random.random() > overtaking_probability:
                        #overtake has failed
                        failure_penalty = random.uniform(0.2, 0.5)
                        driver.race_time = driver_in_front.race_time + failure_penalty
                    else:
                        driver.position -= 1
                        driver.overtakes += 1
                        driver_in_front.position += 1
                        drivers.sort(key=lambda d: d.position)
                else:
                    break
        else:
            break
    drivers.sort(key=lambda d: d.position)
    return drivers




def calculate_pit_stops(drivers, race, lap, num_laps):
    if (num_laps - lap) > 10:
        for driver in drivers:
            if driver.pit_lap:
                if driver.expected_strategy == None:
                    driver.compound = get_next_compound(driver.compound)
                else:
                    try:
                        driver.compound = driver.expected_strategy[driver.stint_number]
                    except IndexError:
                        driver.compound = get_next_compound(driver.compound)
                driver.stint_number += 1
                driver.compounds.append(driver.compound)
                average_pit_loss = get_avg_pit_loss(race)
                driver.race_time += average_pit_loss
                driver.current_lap_time += average_pit_loss
                driver.stint_lap = 0
                driver.pit_laps.append(lap)
    drivers.sort(key=lambda d: d.race_time)
    return drivers





def log_lap_data(drivers):
    for driver in drivers:
        driver.lap_times.append(driver.current_lap_time)


#Main method for simulating the entire race. All other methods can be called from this. 
def simulate_race(race, year, num_laps, best_strategy):
    #Initialise the drivers in their starting order
    drivers, number_of_sectors = initialise_starting_variables(race, year, best_strategy)
    for lap in range(num_laps):
        isolated_sectors = {}
        for driver in drivers:
            driver.current_lap += 1
            driver.stint_lap += 1
            driver.current_lap_time = 0
            initial_lap_time, sector_times = simulate_sector_times(driver, race)
            isolated_sectors[driver.driver_id] = {
                "lap": lap,
                "sectors": sector_times,
                "initial_lap_time": initial_lap_time
            }
        for sector_number in range(number_of_sectors):
            calculate_gaps_to_in_front(drivers)
            for driver in drivers:
                recalculated_sector_time = 0
                if (lap == 0 and sector_number == 0):
                    driver.current_lap_time += driver.starting_sector
                    driver.race_time += driver.starting_sector
                else:
                    current_sector_type = TRACK_SECTORS[race][sector_number]["type"]
                    drs_sector = TRACK_SECTORS[race][sector_number]["DRS"]
                    isolated_sector_time = isolated_sectors[driver.driver_id]['sectors'][sector_number]
                    if current_sector_type == "straight":
                        if drs_sector:
                            driver.drs = is_DRS_available(driver.gap_to_in_front, lap)
                            if driver.drs:
                                recalculated_sector_time = get_DRS_affect(race, sector_number, isolated_sector_time)
                                driver.drs = False
                            else:
                                recalculated_sector_time = get_slipstream_affect(race, sector_number, isolated_sector_time, driver.gap_to_in_front)
                        else:
                            recalculated_sector_time = get_slipstream_affect(race, sector_number, isolated_sector_time, driver.gap_to_in_front)
                    else:
                        recalculated_sector_time = get_following_cornering_affect(race, sector_number, isolated_sector_time, driver.gap_to_in_front)
                    driver.current_lap_time += recalculated_sector_time
                    driver.race_time += recalculated_sector_time
            drivers = calculate_overtakes(drivers, race, sector_number)
        drivers = calculate_pit_stops(drivers, race, lap, num_laps)
        log_lap_data(drivers)
    return drivers, race


def write_data_to_csv(drivers, simulation_number, file_path):
    if drivers:
        file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
        with open(f'{file_path}', 'a', newline='') as csvfile:
            fieldnames = ["race_number", "Driver", "starting_position", "finishing_position", "race_time", "strategy", "pit_laps", "overtakes", "number_of_laps_completed", "lap_times"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for driver in drivers:
                writer.writerow({"race_number": simulation_number, "Driver": driver.driver_id, "starting_position": driver.grid_slot, "finishing_position": driver.position,
                                "race_time": driver.race_time, "strategy": driver.compounds, "pit_laps": driver.pit_laps, "overtakes": driver.overtakes, "number_of_laps_completed": len(driver.lap_times), "lap_times": driver.lap_times})


def calculate_best_strategy(results, driver_list):
    average_times = {}
    best_average_times = {}
    sorted_best_average_times = {}
    for driver in driver_list:
        average_times[driver] = {}
        for strategy_tuple in results[driver]:
            average_time = sum(results[driver][strategy_tuple]) / len(results[driver][strategy_tuple])
            average_times[driver][strategy_tuple] = average_time
    for driver in average_times:
        best_average_times[driver] = {}
        best_strategy = min(average_times[driver], key=average_times[driver].get)
        best_average_times[driver][best_strategy] = average_times[driver][best_strategy]
        sorted_best_average_times = OrderedDict(sorted(best_average_times.items(), key=lambda x: list(x[1].values())[0]))
    return sorted_best_average_times


def create_results_dictionary(driver_list, preliminary_results_df):
    results = {}
    for driver in driver_list:
        results[driver] = {}
    
    for simulation_number in preliminary_results_df['race_number'].unique():
        race_data = preliminary_results_df[preliminary_results_df['race_number']==simulation_number]
        for index, row in race_data.iterrows():
            driver_name = row['Driver']
            strategy_list = ast.literal_eval(row['strategy'])
            strategy_tuple = tuple(strategy_list)
            race_time = row['race_time']
            if strategy_tuple in results[driver_name]:
                results[driver_name][strategy_tuple].append(race_time)
            else:
                results[driver_name][strategy_tuple] = [race_time]
    return results

#Runs the simulations without the best strategy dictionary. 
def run_preliminary_simulations(race_name, number_of_simulations):
    number_of_laps = get_number_of_laps(race_name)
    for i in range(number_of_simulations):
        simulated_order, race = simulate_race(race_name, 2024, number_of_laps, None)
        write_data_to_csv(simulated_order, i, resource_path(f'Data/{race_name}_preliminary_results.csv'))

#Runs the simulations with the selected best strategy. 
def run_final_simulations(race_name, number_of_simulations):
    number_of_laps = get_number_of_laps(race_name)
    preliminary_results_df = pd.read_csv(resource_path(f'Data/{race_name}_preliminary_results.csv'))
    driver_list = find_driver_list(race_name)
    preliminary_results_dictionary = create_results_dictionary(driver_list, preliminary_results_df)
    best_strategy_dictionary = calculate_best_strategy(preliminary_results_dictionary, driver_list)
    for i in range(number_of_simulations):
        optimised_simulated_drivers, race = simulate_race(race_name, 2024, number_of_laps, best_strategy_dictionary)
        write_data_to_csv(optimised_simulated_drivers, i, resource_path(f'Data/{race_name}_final_results.csv'))

#Executes the whole file. This is the method called from the GUI window. 
def run_simulation(race_name, number_of_initial_simulations, number_of_final_simulations):
    run_preliminary_simulations(race_name, number_of_initial_simulations)
    run_final_simulations(race_name, number_of_final_simulations)