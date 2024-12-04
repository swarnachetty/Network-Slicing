# -*- coding: utf-8 -*-

"""
Created on Thu Nov 14 10:13:17 2024

@author: lzr511
"""

# Imports
import numpy as np
import matplotlib.pyplot as plt


# Define a basic structure for a service with QoS requirements
class Service:
    def __init__(self, name, data_rate, num_rbs, bandwidths, latency, availability, reliability, jitter, packet_loss, flow_behaviour, priority, connection_density): #, num_service_per_episode):
        self.name = name
        self.data_rate = data_rate #mbps
        self.bandwidth = bandwidths
        self.num_rbs = num_rbs
        self.latency = latency  # in ms
        self.availability = availability  # in percentage
        self.reliability = reliability 
        self.jitter = jitter
        self.packet_loss = packet_loss
        self.flow_behaviour = flow_behaviour
        self.priority = priority
        self.connection_density = connection_density
        self.num_service_per_episode = num_service_per_episode

    # def __repr__(self):
    #     return (f"{self.name}"
    #             f"Num.of Service: {self.num_service_per_episode}\n"
    #             f"Bandwidth={self.bandwidth} Mbps \n"
    #             f"Latency={self.latency} ms \n"
    #             f"Availability={self.availability}% \n"
    #             f"Reliability={self.reliability} \n"
    #             f"Jitter={self.jitter} \n"
    #             f"Packet loss={self.packet_loss} \n"
    #             f"Priority={self.priority} \n"
    #             f"Connection Density={self.connection_density} \n"
    #             )

# Generate a list of services with random QoS
def repo_generate_services(num_service_per_episode, num_episode):

    dict_service = {}
    
    for i in range(num_episode):
        name_episode = f"Episode_{i}"
        services = []
        
        # Setting the seed for reproducibility
        #np.random.seed(42)
#
        # Generating distributions
       
        # Bandwidth
        min_bandwidth_mhz, max_bandwidth_mhz = 10, 100 #mhz
        spectral_efficiency_bps_hz = 2  # Example: 2 bps/Hz
        overhead_percentage = 10  # Assuming 10% network overhead
        bandwidth = np.random.randint(min_bandwidth_mhz, max_bandwidth_mhz, size=num_service_per_episode) 
        
        # Convert bandwidth from MHz to Hz (for spectral efficiency calculations)
        bandwidths_hz = bandwidth * 1e6  # 1 MHz = 1e6 Hz
        # Calculate raw data rates in bps considering spectral efficiency
        raw_data_rates_bps = bandwidths_hz * spectral_efficiency_bps_hz
        
        #Throughput
        # Convert raw data rates to Mbps and consider network overhead
        data_rate = (raw_data_rates_bps / 1e6) * (1 - overhead_percentage / 100)
        
        # Define subcarrier spacing for numerology 1, which is 30 kHz
        subcarrier_spacing_khz = 30
        
        # Each Resource Block consists of 12 subcarriers
        rb_bandwidth_khz = 12 * subcarrier_spacing_khz
        
        # Convert the bandwidth from MHz to kHz
        total_bandwidth_khz = bandwidth * 1000
        
        # Calculate the number of RBs needed
        num_rbs = total_bandwidth_khz / rb_bandwidth_khz
        

        
        # Latency
        latency = np.random.normal(loc= 15, scale=3, size=num_service_per_episode) 
        
        # Availability
        #availability = np.random.uniform(99.0, 99.999, size=num_service_per_episode)
        beta_values_availability = np.random.beta(a=2, b=2, size=num_service_per_episode)  
        # Convert beta distribution values from a range of 0-1 to 99.0%-99.99999%
        min_val = 99.9
        max_val = 99.999
        availability = min_val + (max_val - min_val) * beta_values_availability
        # Round the availability values for more realistic percentage display
        rounded_availability = np.round(availability, 3)  # Rounded to five decimal places    
              
        # Reliability        
        reliability = np.random.beta(a=5, b=1, size=num_service_per_episode) * 100 
        
        #Jitter
        jitter = np.random.normal(loc=4, scale=10, size=num_service_per_episode)  # Jitter

        #Packet Loss
        packet_loss = np.random.beta(a=2, b=50, size=num_service_per_episode) * 100  # Packet Loss
        
        #Flow Behavious
        flow_behaviour = np.random.normal(loc=0.5, scale=0.1, size=num_service_per_episode) # Flow Behaviour
        
        #Priority
        priority = np.random.normal(loc=5, scale=2, size=num_service_per_episode)
        
        # Connection Density
        connection_density = np.random.lognormal(mean=4, sigma=1.2, size=num_service_per_episode)  # Connection Density
           
        
        
        
        
        for j in range(num_service_per_episode):
            service = Service(f"SFC{j}", data_rate[j], bandwidth[j], num_rbs[j], latency[j], rounded_availability[j], reliability[j],
                              jitter[j], packet_loss[j], flow_behaviour[j], priority[j], connection_density[j])
            
            services.append(service)
        dict_service[name_episode] = services
                
        
        
        # # Recreating histograms for each distribution with grids added

        # # Creating histograms for each distribution
        # fig, axs = plt.subplots(3, 3, figsize=(15, 12))

        # axs[0, 0].hist(bandwidth, bins=30, color='blue', alpha=0.7)
        # axs[0, 0].set_title('Bandwidth Distribution (Mbps)')
        # axs[0, 0].grid(True)

        # axs[0, 1].hist(latency, bins=30, color='green', alpha=0.7)
        # axs[0, 1].set_title('Latency Distribution (ms)')
        # axs[0, 1].grid(True)

        # axs[0, 2].hist(rounded_availability, bins=30, color='red', alpha=0.7)
        # axs[0, 2].set_title('Availability Distribution (%)')
        # axs[0, 2].grid(True)

        # axs[1, 0].hist(reliability, bins=30, color='purple', alpha=0.7)
        # axs[1, 0].set_title('Reliability Distribution (%)')
        # axs[1, 0].grid(True)

        # axs[1, 1].hist(jitter, bins=30, color='orange', alpha=0.7)
        # axs[1, 1].set_title('Jitter Distribution (ms)')
        # axs[1, 1].grid(True)

        # axs[1, 2].hist(packet_loss, bins=30, color='brown', alpha=0.7)
        # axs[1, 2].set_title('Packet Loss Distribution (%)')
        # axs[1, 2].grid(True)

        # axs[2, 0].hist(connection_density, bins=30, color='cyan', alpha=0.7)
        # axs[2, 0].set_title('Connection Density Distribution (devices/km²)')
        # axs[2, 0].grid(True)

        # # Hide unused subplots
        # axs[2, 1].axis('off')
        # axs[2, 2].axis('off')

        # fig.tight_layout()
        # plt.show()
        
    return dict_service

# Example usage
num_service_per_episode = 10
num_episode = 1
services_dictionary = repo_generate_services(num_service_per_episode, num_episode) # generarting the service repository.
for episode, services in services_dictionary.items():
    print(f"{episode}")

    for service in services:
        print(f"  {service.name}:"
               f" Bandwidth={service.bandwidth}Mhz , " 
               f"data rate = {service.data_rate} mbps,"
               f"requires RB: {service.num_rbs}"
               #f"Latency={service.latency} ms",
              #f"Priority = {service.priority}"
              )  
    
# class NetworkSlice:
#     def __init__(self, name, bandwidth, latency, reliability, availability, connection_density=None):
#         self.name = name
#         self.bandwidth = bandwidth
#         self.latency = latency
#         self.reliability = reliability
#         self.availability = availability
#         self.connection_density = connection_density

#     def __str__(self):
#         return (f"Slice Name: {self.name}\n"
#                 f"  Bandwidth: {self.bandwidth} Mbps\n"
#                 f"  Latency: {self.latency} ms\n"
#                 f"  Reliability: {self.reliability}%\n"
#                 f"  Availability: {self.availability}%\n"
#                 f"  Connection Density: {self.connection_density} devices/km²\n")

# # Create slices based on QoS requirements
# slices = [
#     NetworkSlice("eMBB", 1000, 10, 99.9, 99.95),
#     NetworkSlice("URLLC", 100, 1, 99.9999, 99.999),
#     NetworkSlice("mMTC", 10, 50, 99.5, 99.9, 1000000),
#     NetworkSlice("O-RAN Flexible", 500, 5, 99.95, 99.98)
# ]

# # Display the slices
# for slice in slices:
#     print(slice)


