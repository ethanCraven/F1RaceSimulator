import constants
import importlib
import Track_sectors
importlib.reload(constants)
importlib.reload(Track_sectors)
from constants import TYRE_PARAMS, DRIVER_CONSTANTS, AVG_FUEL_LOSS
from Track_sectors import TRACK_SECTORS
import pandas as pd
import random


driver_efficiency = pd.read_csv('/home/ethan/RaceSimulator/FormulaOneRaceSimulator/Data/driver_efficiency.csv')

class Driver:
    def __init__(self, driver_id, base_lap_time, fuel_level, starting_compound, race_name, expected_strategy):
        self.driver_id = driver_id
        self.base_lap_time = base_lap_time
        self.fuel_level = fuel_level
        self.compound = starting_compound
        self.lap_times = []
        self.position = None
        self.race_time = 0
        self.race_name = race_name
        self.current_lap = 0
        self.current_lap_time = 0
        self.stint_lap = 0
        self.race_pace_multiplier = self.get_race_pace()
        self.drs = False
        self.grid_slot = 0 
        self.starting_distance = 0
        self.starting_sector = 0
        self.starting_compound = starting_compound
        self.pit_laps = []
        self.compounds = []
        self.overtakes = 0
        self.gap_to_in_front = 0
        self.driver_in_front = None
        self.pit_lap = False
        self.expected_strategy = expected_strategy
        self.stint_number = 1

    #Method that gets the race pace value associated with the driver.
    def get_race_pace(self):
        try:
            race_pace = driver_efficiency.loc[driver_efficiency["driver"] == f"{self.driver_id}", 'efficiency_score'].values[0]
        except IndexError:
            race_pace = DRIVER_CONSTANTS[self.driver_id]["pace"]
        return race_pace

    #Method that simulates the lap time and then the sector times of that lap. 
    def simulate_sector_times(self, lap_number, race_name):
        fuel_affect = self.fuel_affect()
        tyre_affect = self.get_tyre_affect(lap_number, race_name)
        lap_time = self.base_lap_time + fuel_affect + tyre_affect
        #Add in an element of randomness
        lap_time = lap_time * random.uniform(0.99,1.01)
        self.fuel_level = self.get_fuel_for_lap(race_name)
        self.current_lap += 1
        sector_times = self.simulate_sectors(lap_time, race_name)
        return lap_time, sector_times

    #Method that calculates a laps individual sector times.
    def simulate_sectors(self, lap_time, race_name):
        lap_sector_times = []
        sectors = TRACK_SECTORS[race_name]
        for sector in sectors:
            sector_time = lap_time * sector["%Lap"]
            lap_sector_times.append(sector_time)
        return lap_sector_times


    #returns the fuel effect. Fuel must always be in kilograms. 
    def fuel_affect(self):
        return self.fuel_level * 0.03

    #Method that calculates the current tyre affect for the lap. 
    def get_tyre_affect(self, lap_number, race_name):
        tyre_affect = 0
        params = TYRE_PARAMS[race_name][self.compound]
        driver_params = self.race_pace_multiplier
        tyre_affect = params["base"] + params["linear"] * lap_number + params["quadratic"] * (lap_number ** 2)
        total_tyre_affect = tyre_affect * driver_params
        self.is_time_to_pit(total_tyre_affect, race_name)
        return total_tyre_affect
    
    #Method that determines whether it is time to pit depending on the current tyre affect and threshold. 
    def is_time_to_pit(self, tyre_affect, race_name):
        base_tyre_affect = TYRE_PARAMS[race_name][self.compound]["base"]
        threashold = TYRE_PARAMS[race_name][self.compound]["%Threshold"]
        random_multiplier = random.uniform(1.01, 1.2)
        if (tyre_affect / base_tyre_affect) > (threashold * random_multiplier) :
            self.pit_lap = True
        else:
            self.pit_lap = False


    #This takes away the fuel per lap for the grand prix. 
    def get_fuel_for_lap(self, race):
        average_loss_per_lap = AVG_FUEL_LOSS[race]
        self.fuel_level -= float(average_loss_per_lap)
        return self.fuel_level
    
    #Calcualtes the starting distance for the driver to add to the first sector. 
    def get_starting_distance(self, race):
        distance = TRACK_SECTORS[race][0]["end"] - TRACK_SECTORS[race][0]["start"]
        grid_distance = self.grid_slot * 8
        distance += grid_distance
        return distance