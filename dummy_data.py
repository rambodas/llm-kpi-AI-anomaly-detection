import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define date range
start_date = datetime(2025, 6, 1)
end_date = datetime(2025, 6, 28)
date_range = pd.date_range(start=start_date, end=end_date)

# Define lat-long regions
locations = {
    "India": {"lat_range": (8.0, 37.0), "lon_range": (68.0, 97.0)},
    "Dubai": {"lat_range": (25.0, 25.5), "lon_range": (55.0, 55.5)},
    "Mauritius": {"lat_range": (-20.2, -19.8), "lon_range": (57.3, 57.8)},
    "Sri Lanka": {"lat_range": (5.9, 9.8), "lon_range": (79.8, 81.9)},
}

# Define base login volumes
base_logins = {
    "India": (800, 1200),       # Consistent volume
    "Dubai": (10, 30),          # Low volume with spike
    "Mauritius": (5, 15),
    "Sri Lanka": (5, 15),
}

# Define anomaly spikes
anomalies = {
    "Dubai": {"date": datetime(2025, 6, 10), "volume": 150},
    "Mauritius": {"date": datetime(2025, 6, 15), "volume": 100},
    "Sri Lanka": {"date": datetime(2025, 6, 20), "volume": 120},
}

# Generate login data
data = []

for date in date_range:
    for region, bounds in locations.items():
        base_low, base_high = base_logins[region]
        count = random.randint(base_low, base_high)

        # Inject anomaly if this is the spike date
        if region in anomalies and date == anomalies[region]["date"]:
            count += anomalies[region]["volume"]

        for _ in range(count):
            lat = random.uniform(*bounds["lat_range"])
            lon = random.uniform(*bounds["lon_range"])
            data.append([date, lat, lon, region])

# Create DataFrame
df = pd.DataFrame(data, columns=["date", "latitude", "longitude", "region"])

# Save to CSV
df.to_csv("dummy_login_data_multi_region.csv", index=False)
print("✅ dummy_login_data_multi_region.csv created.")
