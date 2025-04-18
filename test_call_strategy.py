import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from typing import List

# Generate price data starting near your bounds
df = pd.DataFrame({'price': 10.5 + np.cumsum(np.random.randn(500) * 0.01)})

# Parameters
window_size = 100
smooth_window = 5
min_price = 10.5
max_price = 11.0

# Container to store qualifying timestamps and maxima points
local_max_counts = []
all_maxima = []  # To store all maxima points for plotting

for i in range(window_size, len(df)):
    window = df.iloc[i - window_size:i].copy()
    prices = window['price'].values

    # Step 1: Smooth using moving average
    smoothed = np.convolve(prices, np.ones(smooth_window) / smooth_window, mode='valid')

    # Step 2: Approximate derivative
    derivative = np.diff(smoothed)

    # Step 3: Detect local maxima
    local_max_idx = []
    for j in range(1, len(derivative) - 1):
        if derivative[j - 1] > 0 > derivative[j]:
            local_max_idx.append(j)

    # Step 4: Get max values and filter by price bounds
    local_max_vals = [smoothed[j] for j in local_max_idx]
    filtered_vals = [v for v in local_max_vals if min_price <= v <= max_price]

    # Store all maxima for plotting
    for idx in local_max_idx:
        # Get the corresponding index in the original DataFrame
        original_idx = window.index[idx + smooth_window // 2]
        all_maxima.append((original_idx, smoothed[idx]))

    # Step 5: Check if 3+ maxima lie within the interval
    if len(filtered_vals) >= 3:
        local_max_counts.append((df.index[i], len(filtered_vals)))

# Print results
print(f"Found {len(local_max_counts)} qualifying windows")
for t, count in local_max_counts:
    print(f"{t}: {count} local maxima in price range [{min_price}, {max_price}]")
