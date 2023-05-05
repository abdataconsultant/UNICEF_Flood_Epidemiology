import requests
import richdem
import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Accept user input for the geographic extent and output file name
south = float(input("Enter south latitude: "))
north = float(input("Enter north latitude: "))
west = float(input("Enter west longitude: "))
east = float(input("Enter east longitude: "))
output_file = input("Enter output file name: ")

# Define the API endpoint URL and parameters
API_KEY = "7aabc73c727819d3ddbadd7a8772d091"
url = "https://portal.opentopography.org/API/globaldem"
params = {
    "demtype": "SRTMGL1",
    "south": south,
    "north": north,
    "west": west,
    "east": east,
    "outputFormat": "GTiff",
    "API_Key": API_KEY,
}

# Send a GET request to the API endpoint with the parameters
response = requests.get(url, params=params)

# Check for errors in the API response
if response.status_code != 200:
    print(f"Error: API returned status code {response.status_code}")
else:
    # Save the response content (DEM) to a file
    with open(output_file + ".tif", "wb") as f:
        f.write(response.content)

filename = 'output_dem.tif' #f"{output_file}.tif"
dem = rio.open(filename)
dem_array = dem.read(1).astype("float64")

fig, ax = plt.subplots(1, figsize=(12, 12))
show(dem_array, cmap="Greys_r", ax=ax)
plt.axis("off")
plt.show()

fig, ax = plt.subplots(1, figsize=(12, 12))
show(dem_array, cmap="Greys_r", ax=ax)
show(dem_array, contour=True, ax=ax, linewidths=0.7)
plt.axis("off")
plt.show()

dem_richdem = richdem.rdarray(dem_array, no_data=-9999)
fig = richdem.rdShow(dem_richdem, axes=False, cmap="bone", figsize=(16, 10))

dem_slope = richdem.TerrainAttribute(dem_richdem, attrib="slope_degrees")
richdem.rdShow(dem_slope, axes=False, cmap="YlOrBr", figsize=(16, 10))

dem_curvature = richdem.TerrainAttribute(dem_richdem, attrib="curvature")
richdem.rdShow(dem_curvature, axes=False, cmap="YlOrBr", figsize=(16, 10))

dem_filled = richdem.FillDepressions(dem_richdem, in_place=False)
dem_filled_fig = richdem.rdShow(
    dem_filled,
    ignore_colours=[0],
    axes=False,
    cmap="jet",
    vmin=fig["vmin"],
    vmax=fig["vmax"],
    figsize=(16, 10),
)

accum_freeman = richdem.FlowAccumulation(dem_filled, method="Freeman", exponent=1.1)

richdem.rdShow(
    accum_freeman,
    zxmin=450,
    zxmax=550,
    zymin=550,
    zymax=450,
    figsize=(8, 5.5),
    axes=False,
    cmap="jet",
)

slope_radians = richdem.TerrainAttribute(dem_richdem, attrib="slope_radians")
twi = np.log(
    accum_freeman / (np.tan(slope_radians) + 30)
)  # 30 is dem value should come from variable to adjust the pixel size
richdem.rdShow(twi)

spi = accum_freeman * (np.tan(slope_radians))

richdem.rdShow(spi)
