import pandas as pd
import Calibrate
import time

# Read CSV data into DataFrame
df = pd.read_csv('../autopoints.csv')

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Extract current values from the row
    current_vals = row.tolist()
    
    # Call the calibration functions as specified
    Calibrate.set_servo_pulse(0, current_vals[0])
    Calibrate.set_servo_pulse(1, current_vals[1])
    Calibrate.set_servo_pulse(14, current_vals[2])
    Calibrate.set_servo_pulse(15, current_vals[3])
    
    # Wait for 1 second before processing the next row
    time.sleep(1)
