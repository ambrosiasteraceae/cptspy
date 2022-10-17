import pandas as pd
from pyproj import Proj
import matplotlib.pyplot as plt
import folium

proj_fn = Proj(proj='utm', zone=40, ellps='WGS84', preserve_units=False)

# Load data frame
df = pd.read_excel("nawras_bhs_coords.xlsx", skiprows=1, sheet_name=['Sheet1', 'Sheet2'])

ids_first_sheet = list(df['Sheet1']['NO.'])
ids_second_sheet = list(df['Sheet2']['NO.'])


eastings_first_sheet = list(df['Sheet1']['EASTING'])
northings_first_sheet = list(df['Sheet1']['NORTHING'])
eastings_second_sheet = list(df['Sheet2']['EASTING'])
northings_second_sheet = list(df['Sheet2']['NORTHING'])


def convert_to_lat_and_long(easts, norths, proj):
    """Convert a list of eastings & northings
    from Easting / Northing to Longitude and latitude
    into a list of tuples(long,lat)"""
    return [proj(a, b, inverse=True) for a, b in zip(easts, norths)]


coords_piles = convert_to_lat_and_long(eastings_first_sheet, northings_first_sheet, proj_fn)
coords_bhs = convert_to_lat_and_long(eastings_second_sheet, northings_second_sheet, proj_fn)

coords_piles

# Convert to individual list
longs = [i[0] for i in coords_piles] + [j[0] for j in coords_bhs]
lats = [i[1] for i in coords_piles] + [j[0] for j in coords_bhs]

max_longs, min_longs = max(longs), min(longs)
max_lats, min_lats = max(lats), min(lats)

map = folium.Map(min_lat=min_lats, max_lat=max_lats,
                 min_long=min_longs, max_long=max_longs,
                 zoom_start=14, control_scale=True)

for i, t in enumerate(coords_piles):
    folium.Marker(t[::-1], radius=5, color='blue', popup=ids_first_sheet[i], fill=True,
                  fill_color="#63ebe4").add_to(map)

for i, t in enumerate(coords_bhs):
    folium.Marker(t[::-1], radius=2, color='green', popup=ids_second_sheet[i], fill=True,
                  fill_color="#eb6363",
                  icon=folium.Icon(color='green', angle=30, size=2)).add_to(map)

map