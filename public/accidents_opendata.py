#!/usr/bin/env python3

import pandas as pd

# Read the whole dataset
df = pd.read_csv("accidents_opendata.csv", index_col=0, low_memory=False)

# Drop the unused columns
df = df.drop(columns=["neighborhood_id", "longitude", "latitude", "district_id"])

# Convert the coordinates to float
df = df.assign(**{
    f"utm_coordinate_{ax}": df[f"utm_coordinate_{ax}"].apply(
        lambda v: float(v.replace(",", ".") if isinstance(v, str) else v)
    ).apply(
        lambda v: v / 10 if v > 1000000 else v
    )
    for ax in ['x', 'y']
})

# Oddly, x and y are flipped for half of the records
def fix_coords(r: pd.Series):
    if r["utm_coordinate_x"] > r["utm_coordinate_y"]:
        r["utm_coordinate_x"], r["utm_coordinate_y"] = r["utm_coordinate_y"], r["utm_coordinate_x"]
    return r

df = df.apply(fix_coords, axis=1)

# Drop coordinates < 0
df = df.query("utm_coordinate_x > 0 and utm_coordinate_y > 0")

# Use the column year, month, day, and hour to produce a datetime column
df["datetime"] = pd.to_datetime(df[["year", "month", "day", "hour"]].astype(int).astype(str).agg('-'.join, axis=1), format='%Y-%m-%d-%H')

# Convert the columns year, month, day, and hour to integers
df[["year", "month", "day", "hour"]] = df[["year", "month", "day", "hour"]].astype(int)

# Make a column with just the YYYY-MM by appending the year and month columns
df["year_month"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)
print(df["year_month"].value_counts())

# Write to feather
df.to_feather("accidents_opendata.feather")
