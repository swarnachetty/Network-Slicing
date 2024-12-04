# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:15:33 2024

@author: lzr511
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, datetime


def generate_complex_traffic_data(start_date, num_days, peak_traffic):
    # Create a time series for the days specified
    date_range = pd.date_range(start=start_date, periods=num_days*24, freq='H')
    # Initialize the data array
    data = np.zeros(num_days * 24)
    
    for i in range(num_days * 24):
        # Determine the hour and day of the week
        hour = i % 24
        day_of_week = (i // 24) % 7

        # Base traffic volume is affected by the day of the week
        if day_of_week < 5:  # Weekday
            base_traffic = peak_traffic
        else:  # Weekend
            base_traffic = peak_traffic * 0.7
        
        # Hourly adjustments to the base traffic
        if 7 <= hour < 9:  # Morning peak hours
            traffic = np.random.normal(loc=0.8 * base_traffic, scale=0.1 * base_traffic)
        elif 9 <= hour < 17:  # Day time slightly lower than peak
            traffic = np.random.normal(loc=0.6 * base_traffic, scale=0.1 * base_traffic)
        elif 17 <= hour < 19:  # Evening peak hours
            traffic = np.random.normal(loc=0.9 * base_traffic, scale=0.1 * base_traffic)
        else:  # Off hours
            traffic = np.random.normal(loc=0.3 * base_traffic, scale=0.05 * base_traffic)
        
        # Introduce random spikes and anomalies
        if np.random.rand() < 0.01:  # 1% chance of a spike
            traffic *= np.random.uniform(1.5, 3.0)  # Spike can increase traffic by 50% to 200%
        
        data[i] = max(0, traffic)  # Ensure traffic does not go negative

    return pd.Series(data, index=date_range)


# Set parameters
start_date = datetime.now().strftime('%Y-%m-%d')
num_days = 30  # Generate data for 30 days for better visualization
peak_traffic = 1000  # Peak traffic volume

# Generate traffic data
traffic_data = generate_complex_traffic_data(start_date, num_days, peak_traffic)

# Plot the data
plt.figure(figsize=(14, 7))
plt.plot(traffic_data, label='Network Traffic Volume', color='blue')
plt.title('Complex Synthetic Network Traffic Data')
plt.xlabel('Time')
plt.ylabel('Traffic Volume')
plt.legend()
plt.grid(True)
plt.show()
