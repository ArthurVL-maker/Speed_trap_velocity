# speed_trap_velocity.py
# ----------------------------------------------------------------------------------------------------------
# Uses the recorded signals from the speed trap to calculate the velocity of the striker bar during
# split-Hopkinson pressure bar experiments.

# INPUTS:
# - raw_file: Path to csv file containing oscilloscope data columns Time, Ch1, Ch2, Ch3, Ch4 (string).

# OUTPUTS:
# - velocity: speed of the striker bar.

# Authors: Arthur van Lerberghe (avanlerberghe1@sheffield.ac.uk) & Kin Shing Oswald Li (ksoli1@sheffield.ac.uk)
# ----------------------------------------------------------------------------------------------------------
# Imported modules:
import pandas as pd
import numpy as np


def speed_trap_velocity(raw_file):
    trap_distance = 50  # Distance between speed traps, mm
    trigger_voltage = 24  # Voltage level triggering pulse, V

    # Read the csv file and extract necessary columns:
    raw_data = pd.read_csv(raw_file, sep=';', skiprows=9, header=None)  # Read csv file
    time = raw_data.iloc[:, 0]  # Time, s
    gauge_signal = raw_data.iloc[:, 1:3]

    # Find the index where gauge signal exceeds the trigger voltage:
    front_trigger_idx = np.argmax(gauge_signal.iloc[:, 0] > trigger_voltage)
    back_trigger_idx = np.argmax(gauge_signal.iloc[:, 1] > trigger_voltage)

    # Calculate the time at which each signal triggers:
    front_trigger_time = time[front_trigger_idx]
    back_trigger_time = time[back_trigger_idx]

    # Calculate the velocity of the striker bar:
    difference = abs(back_trigger_time - front_trigger_time)  # Difference between trigger times, s
    velocity = (trap_distance / difference) / 10 ** 3  # Velocity of striker bar, m/s

    return f'Velocity of striker bar: {round(velocity, 3)} m/s'
