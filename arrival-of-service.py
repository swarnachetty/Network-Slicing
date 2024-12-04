# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 11:40:18 2024

@author: lzr511
"""

import numpy as np

# Define services and their average request rates (lambda)
services = {
    'Video Streaming': 5,  # average 5 requests per time unit
    'Web Browsing': 10,    # average 10 requests per time unit
    'File Download': 2     # average 2 requests per time unit
}

# Simulate service requests for a given time period
def simulate_service_requests(duration):
    # Logs to store service request counts
    print(f"services: {services}")
    request_counts = {service: 0 for service in services}
    print(f"request_counts: {request_counts}")

    # Simulate each service request over the specified duration
    for time in range(duration):
        for service, lambda_rate in services.items():
            # Number of requests in the current time unit
            num_requests = np.random.poisson(lambda_rate)
            request_counts[service] += num_requests
            print(f"Time {time+1}: {num_requests} new requests for {service}")

    # Summary of requests over the entire duration
    print("\nSummary of requests over the duration:")
    for service, count in request_counts.items():
        print(f"{service}: {count} requests")

# Example usage: Simulate service requests over 10 time units
simulate_service_requests(10)
