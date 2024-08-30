import pandas as pd 
import cartopy.crs as ccrs 
import cartopy.feature as cfeature 
import matplotlib.pyplot as plt 
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Load bird tracking data from CSV file
birddata = pd.read_csv("bird_tracking.csv")

# Extract unique bird names from the data
bird_names = pd.unique(birddata.bird_name) 

# Specify the map projection for the plot
proj = ccrs.Mercator()  
  
# Create a new figure with specified size
fig = plt.figure(figsize=(10, 10)) 

# Create an axes object with the specified projection
ax = plt.axes(projection=proj) 

# Set the geographical extent of the plot (lon_min, lon_max, lat_min, lat_max)
ax.set_extent((-25.0, 20.0, 52.0, 10.0)) 

# Add geographic features to the plot
ax.add_feature(cfeature.LAND) 
ax.add_feature(cfeature.OCEAN) 
ax.add_feature(cfeature.COASTLINE) 
ax.add_feature(cfeature.BORDERS, linestyle=':') 

# Plot bird tracking data
for name in bird_names: 
    ix = birddata['bird_name'] == name 
    x, y = birddata.longitude[ix], birddata.latitude[ix] 
    ax.plot(x, y, '.', transform=ccrs.PlateCarree(), label=name) 

# Add a legend to the plot
plt.legend(loc="upper left") 

# Initialize the geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Event handler for mouse clicks
def onclick(event):
    if event.xdata is None or event.ydata is None:
        print("Click was outside the axes")
        return

    # Convert the mouse click location to geographic coordinates
    lon, lat = ccrs.PlateCarree().transform_point(event.xdata, event.ydata, proj)

    # Check if the coordinates are valid
    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        print("Invalid coordinates")
        return

    try:
        location = geolocator.reverse((lat, lon), language='en', timeout=10)
        if location and location.raw.get('address'):
            country = location.raw['address'].get('country', 'Unknown')
            print(f"Coordinates: ({lon:.2f}, {lat:.2f}) - Country: {country}")
            # Add text annotation to the plot
            ax.text(lon, lat, country, transform=ccrs.PlateCarree(), fontsize=12, color='red', bbox=dict(facecolor='white', alpha=0.5))
            plt.draw()
        else:
            print(f"Coordinates: ({lon:.2f}, {lat:.2f}) - Country: Unknown")
    except GeocoderTimedOut:
        print("Geocoding service timed out. Try again.")
    except GeocoderServiceError as e:
        print(f"Geocoding service error: {e}")

# Connect the event handler to the figure
fig.canvas.mpl_connect('button_press_event', onclick)

# Display the plot
plt.show()
