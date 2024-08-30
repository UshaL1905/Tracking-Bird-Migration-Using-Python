import pandas as pd 
import matplotlib.pyplot as plt 
import datetime 
import numpy as np 

# Reading the data from the CSV file
birddata = pd.read_csv("bird_tracking.csv") 

# Extracting unique bird names from the DataFrame
bird_names = pd.unique(birddata.bird_name) 

# Initializing an empty list to store timestamps
timestamps = []

# Looping through each row in the DataFrame
for k in range(len(birddata)):
    # Extracting the date_time string from the DataFrame
    date_str = birddata.date_time.iloc[k]
    
    # Removing the last three characters (milliseconds and space) from the date_time string
    date_str_trimmed = date_str[:-3]
    
    # Converting the trimmed date_time string to a datetime object
    datetime_obj = datetime.datetime.strptime(date_str_trimmed, "%Y-%m-%d %H:%M:%S")
    
    # Appending the datetime object to the timestamps list
    timestamps.append(datetime_obj)

# Creating a pandas Series from the timestamps list with the same index as the DataFrame
timestamp_series = pd.Series(timestamps, index=birddata.index)

# Adding the timestamp Series as a new column in the DataFrame
birddata["timestamp"] = timestamp_series

# Filtering the DataFrame to include only the rows where the bird name is "Nico"
nico_data = birddata[birddata.bird_name == "Eric"]

# Extracting the timestamp column for the filtered DataFrame
times = nico_data.timestamp

# Initializing an empty list to store elapsed time
elapsed_time = []

# Looping through each timestamp for "Nico"
for time in times:
    # Calculating the elapsed time from the first observation
    elapsed = time - times.iloc[0]
    
    # Appending the elapsed time to the elapsed_time list
    elapsed_time.append(elapsed)

# Converting the elapsed_time list to a NumPy array
elapsed_time_array = np.array(elapsed_time)

# Converting elapsed time from timedelta objects to days
elapsed_time_days = elapsed_time_array / datetime.timedelta(days=1)

# Plotting the elapsed time in days
plt.plot(elapsed_time_days)

# Setting the label for the x-axis
plt.xlabel("Observation")

# Setting the label for the y-axis
plt.ylabel("Elapsed time (days)")

# Displaying the plot
plt.show()
