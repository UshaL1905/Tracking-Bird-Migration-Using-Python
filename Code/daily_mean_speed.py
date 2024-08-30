import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# Load bird tracking data from CSV file
birddata = pd.read_csv("bird_tracking.csv")

# Get unique bird names from the dataset
bird_names = pd.unique(birddata.bird_name)

# Convert date_time strings to datetime objects and create a new 'timestamp' column
timestamps = []
for k in range(len(birddata)):
    # Convert each date_time string to a datetime object, ignoring milliseconds (last 3 characters)
    timestamps.append(datetime.datetime.strptime(birddata.date_time.iloc[k][:-3], "%Y-%m-%d %H:%M:%S"))

# Add the 'timestamp' column to the DataFrame
birddata["timestamp"] = pd.Series(timestamps, index=birddata.index)

# Extract data for a specific bird (e.g., "Eric")
data = birddata[birddata.bird_name == "Eric"]

# Calculate elapsed time since the first timestamp in days
times = data.timestamp
elapsed_time = [time - times.iloc[0] for time in times]
elapsed_days = np.array(elapsed_time) / datetime.timedelta(days=1)

# Initialize variables for calculating daily mean speed
next_day = 1
inds = []
daily_mean_speed = []

# Loop through each timestamp and calculate daily mean speeds
for (i, t) in enumerate(elapsed_days):
    if t < next_day:
        inds.append(i)  # Collect indices of timestamps within the same day
    else:
        # Calculate the mean speed for the collected indices (representing a day)
        daily_mean_speed.append(np.mean(data.speed_2d.iloc[inds]))
        next_day += 1  # Move to the next day
        inds = []  # Reset indices for the next day

# Plotting the daily mean speeds
plt.figure(figsize=(8, 6))
plt.plot(daily_mean_speed, "rs-")  # Plotting daily mean speeds as red squares connected by lines
plt.xlabel("Day")
plt.ylabel("Mean Speed (m/s)")
plt.title("Daily Mean Speeds for Bird Eric")
plt.show()
