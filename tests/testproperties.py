from hypothesis import given, strategies as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import driver
import importlib
importlib.reload(driver)
from driver import Driver
import The_Simulation
import unittest
import constants


class PropertyTests(unittest.TestCase):

    #Makre sure lap times are valid and sectors add up to the lap time
    @given(
            tire=st.sampled_from(["soft", "medium", "hard"]), 
            race_name=st.just("netherlands"),
    )
    def test_simulate_sector_times(self, tire, race_name):
        driver = Driver("lando-norris", 70, 110, tire, race_name)
        lap_time, sector_times = driver.simulate_sector_times(5, race_name)
        self.assertGreater(lap_time, 70)
        reconstructed_lap_time = 0
        for sector in sector_times:
            reconstructed_lap_time += sector
        self.assertAlmostEqual(lap_time, reconstructed_lap_time)


    #Test to make sure different drivers have different lap times on the same tyre
    @given(tire=st.just("soft"), race_name=st.just("netherlands"))
    def test_different_times(self, tire, race_name):
        driver_1 = Driver("lando-norris", 70, 110, tire, race_name)
        driver_2 = Driver("lance-stroll", 70, 110, tire, race_name)
        lap_time_1, sector_times_1 = driver_1.simulate_sector_times(5, race_name)
        lap_time_2, sector_times_2 = driver_2.simulate_sector_times(5, race_name)
        self.assertNotEqual(lap_time_1, lap_time_2)
        for i in range(len(sector_times_1)):
            self.assertNotEqual(sector_times_1[i], sector_times_2[i])




    #Test to retrieve the correct base lap time
    @given(driver=st.just("lando-norris"), race_name=st.just("netherlands"),
           year=st.just(2024))
    def test_get_base_lap(self, race_name, year, driver):
        base_lap_time = The_Simulation.get_base_time(race_name, year, driver)
        self.assertEqual(base_lap_time, 69.673)


    #Test to implement reference base lap time if none was set
    @given(driver=st.just("alexander-albon"), race_name=st.just("netherlands"),
            year=st.just(2024))
    def test_valid_lap_time(self, race_name, year, driver):
        base_lap_time = The_Simulation.get_base_time(race_name, year, driver)
        default_base_lap_time = constants.DEFAULT_BASE_LAP[race_name]
        self.assertEqual(base_lap_time, default_base_lap_time)


    #Test to show the affect of tyre degradation
    @given(race_name=st.just("spain"),
           tire=st.just("soft"))
    def test_tyre_deg(self, race_name, tire):
        driver = Driver("lando-norris", 70, 110, tire, race_name)
        intial_tyre_affect = driver.get_tyre_affect(1, race_name)
        secondary_tyre_affect = driver.get_tyre_affect(5, race_name)
        self.assertGreater(secondary_tyre_affect, intial_tyre_affect)

    #Ensures the driver doesnt pit too early
    @given(race_name=st.just("netherlands"),
           tire=st.just("soft"))
    def test_early_pit(self, race_name, tire):
        driver = Driver("lando-norris", 70, 110, tire, race_name)
        tyre_affect = driver.get_tyre_affect(3, race_name)
        time_to_pit = driver.is_time_to_pit(tyre_affect, race_name)
        self.assertFalse(time_to_pit)


    #Testing accurate pit stop
    @given(race_name=st.just("netherlands"),
        tire=st.just("soft"))
    def test_accurate_pit(self, race_name, tire):
        driver = Driver("lando-norris", 70, 110, tire, race_name)
        tyre_affect = driver.get_tyre_affect(25, race_name)
        time_to_pit = driver.is_time_to_pit(tyre_affect, race_name)
        self.assertFalse(time_to_pit)

    #Test decrease in fuel affect over the race
    @given(race_name=st.just("netherlands"),
        tire=st.just("soft"))
    def test_fuel_affect(self, race_name, tire):
        driver = Driver("lando-norris", 70, 110, tire, race_name)
        fuel_affect = driver.fuel_burn_affect()
        driver.get_fuel_for_lap(race_name)
        second_fuel_affect = driver.fuel_burn_affect()
        self.assertLess(second_fuel_affect, fuel_affect)
        
    
    #Check that DRS applies correctly
    @given(race_name=st.just("netherlands"),
        tire=st.just("soft"))
    def test_drs_affect(self, race_name, tire):
        driver_1 = Driver("lando-norris", 70, 110, tire, race_name)
        driver_1.drs = The_Simulation.is_DRS_available(0.8, 10)
        new_sector_time = The_Simulation.get_DRS_affect(race_name, 6, 15)
        self.assertLess(new_sector_time, 15)

    #Tests that DRS only applies when driver is within 1.0 seconds
    @given(race_name=st.just("netherlands"),
        tire=st.just("soft"))
    def test_drs_availability(self, race_name, tire):
        driver_1 = Driver("lando-norris", 70, 110, tire, race_name)
        driver_1.drs = The_Simulation.is_DRS_available(1.1, 10)
        self.assertFalse(driver_1.drs)


    #Tests that following a car in a cornerning sector applies a time loss
    @given(race_name=st.just("netherlands"),
        tire=st.just("soft"))
    def test_cornering_loss(self, race_name, tire):
        driver_1 = Driver("lando-norris", 70, 110, tire, race_name)
        new_sector_time = The_Simulation.get_following_cornering_affect(race_name, 1, 15, 0.7)
        self.assertGreater(new_sector_time, 15)


    #Tests that the loss can not be more than 0.6
    @given(race_name=st.just("netherlands"),
        tire=st.just("soft"))
    def test_maximum_cornering_loss(self, race_name, tire):
        driver_1 = Driver("lando-norris", 70, 110, tire, race_name)
        new_sector_time = The_Simulation.get_following_cornering_affect(race_name, 1, 15, 0.001)
        self.assertEqual(new_sector_time, 15.6)

    #Tests the lack of cornering loss when cars are further away
    @given(race_name=st.just("netherlands"),
        tire=st.just("soft"))
    def test_no_cornering_loss(self, race_name, tire):
        driver_1 = Driver("lando-norris", 70, 110, tire, race_name)
        new_sector_time = The_Simulation.get_following_cornering_affect(race_name, 1, 15, 10)
        self.assertEqual(new_sector_time, 15)

    #Tests where overtakes are more likely 
    @given(race_name=st.just("netherlands"),
        tire=st.just("soft"))
    def test_overtake_probability(self, race_name, tire):
        driver_1 = Driver("lando-norris", 70, 110, tire, race_name)
        driver_2 = Driver("lance-stroll", 70, 110, tire, race_name)
        driver_1.position = 1
        driver_2.position = 2
        driver_1.race_time = 10
        driver_2.race_time = 9.5
        overtaking_probability_1 = The_Simulation.get_overtake_probability(race_name, 6, driver_2, driver_1)
        overtaking_probability_2 = The_Simulation.get_overtake_probability(race_name, 1, driver_2, driver_1)
        self.assertNotEqual(overtaking_probability_1, overtaking_probability_2)






if __name__ == "__main__":
    unittest.main()