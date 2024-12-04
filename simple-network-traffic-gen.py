# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:14:42 2024

@author: lzr511
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, datetime

def generate_traffic_data(start_date, num_days, peak_traffic):
    # Create a time series for the days specified
    date_range = pd.date_range(start=start_date, periods=num_days*24, freq='H')
    # Initialize the data array
    data = np.zeros(num_days * 24)
    
    for i in range(num_days * 24):
        # Determine the hour of the day
        hour = i % 24
        
        # Generate traffic volume based on typical daily pattern
        if 7 <= hour < 9:  # Morning peak hours
            traffic = np.random.normal(loc=0.8 * peak_traffic, scale=0.1 * peak_traffic)
        elif 9 <= hour < 17:  # Day time slightly lower than peak
            traffic = np.random.normal(loc=0.6 * peak_traffic, scale=0.1 * peak_traffic)
        elif 17 <= hour < 19:  # Evening peak hours
            traffic = np.random.normal(loc=0.9 * peak_traffic, scale=0.1 * peak_traffic)
        else:  # Off hours
            traffic = np.random.normal(loc=0.3 * peak_traffic, scale=0.05 * peak_traffic)
        
        data[i] = max(0, traffic)  # Ensure traffic does not go negative

    return pd.Series(data, index=date_range)

# Set parameters
start_date = datetime.now().strftime('%Y-%m-%d')
num_days = 10  # For example, generate data for 10 days
peak_traffic = 1000  # Peak traffic volume

# Generate traffic data
traffic_data = generate_traffic_data(start_date, num_days, peak_traffic)

# Plot the data
plt.figure(figsize=(14, 7))
plt.plot(traffic_data, label='Network Traffic Volume')
plt.title('Synthetic Network Traffic Data')
plt.xlabel('Time')
plt.ylabel('Traffic Volume')
plt.legend()
plt.grid(True)
plt.show()
