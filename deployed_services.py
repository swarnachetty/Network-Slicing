# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 14:50:05 2024

@author: lzr511
"""


# Imports
import numpy as np
import matplotlib.pyplot as plt


# Define a basic structure for a service with QoS requirements
class Service:
    def __init__(self, name, data_rate, num_rbs, bandwidths, latency, availability, reliability, jitter, packet_loss, flow_behaviour, priority, connection_density, type_slice): #, num_service_per_episode):
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
        self.type_slice = type_slice

# Generate a list of services with random QoS
def repo_generate_services(num_service_per_episode, num_episode):

    dict_service = {}
    
    for i in range(num_episode):
        name_episode = f"Episode_{i}"
        services = []
        
        # Setting the seed for reproducibility
        np.random.seed(42)
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
           
        type_slice = np.random.choice([0, 0], size=num_service_per_episode)
        
        
        
        for j in range(num_service_per_episode):
            service = Service(f"SFC{j}", data_rate[j], 
                                         bandwidth[j], 
                                         num_rbs[j], 
                                         latency[j], 
                                         rounded_availability[j], 
                                         reliability[j],
                                         jitter[j], 
                                         packet_loss[j], 
                                         flow_behaviour[j], 
                                         priority[j], 
                                         connection_density[j],
                                         type_slice[j]
                                         )
            
            services.append(service)
        dict_service[name_episode] = services
                
        
        
        # Recreating histograms for each distribution with grids added

        # Creating histograms for each distribution
        fig, axs = plt.subplots(3, 3, figsize=(15, 12))

        axs[0, 0].hist(bandwidth, bins=30, color='blue', alpha=0.7)
        axs[0, 0].set_title('Bandwidth Distribution (Mbps)')
        axs[0, 0].grid(True)

        axs[0, 1].hist(latency, bins=30, color='green', alpha=0.7)
        axs[0, 1].set_title('Latency Distribution (ms)')
        axs[0, 1].grid(True)

        axs[0, 2].hist(rounded_availability, bins=30, color='red', alpha=0.7)
        axs[0, 2].set_title('Availability Distribution (%)')
        axs[0, 2].grid(True)

        axs[1, 0].hist(reliability, bins=30, color='purple', alpha=0.7)
        axs[1, 0].set_title('Reliability Distribution (%)')
        axs[1, 0].grid(True)

        axs[1, 1].hist(jitter, bins=30, color='orange', alpha=0.7)
        axs[1, 1].set_title('Jitter Distribution (ms)')
        axs[1, 1].grid(True)

        axs[1, 2].hist(packet_loss, bins=30, color='brown', alpha=0.7)
        axs[1, 2].set_title('Packet Loss Distribution (%)')
        axs[1, 2].grid(True)

        axs[2, 0].hist(connection_density, bins=30, color='cyan', alpha=0.7)
        axs[2, 0].set_title('Connection Density Distribution (devices/km²)')
        axs[2, 0].grid(True)

        # Hide unused subplots
        axs[2, 1].axis('off')
        axs[2, 2].axis('off')

        fig.tight_layout()
        plt.show()
        
    return dict_service

# Example usage
num_service_per_episode = 100
num_episode = 1
services_dictionary = repo_generate_services(num_service_per_episode, num_episode) # generarting the service repository.

details_of_service = False #True #False

if details_of_service == True:
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
else:
    pass
    


"""
Task 0: The above SFC or services are assumed to be deployed on to the network (environment)
Task 1: Based on these QoS like the latency, bandwidth... classify these services as URLLC or emBB slice and update to the class service.         
Task 2: In the another file, we have an rough enviroment, allocate each BS certain resources like 278 PRBs to each Basestation. for simplicity we are consider that as URLLC slice only.
Task 3: Each BS PRBs will be distributed as Decicated, Prioritization and Shared. (this is will standared) and our aim is to dynamically change the ratios based on the environment.network conditions. 
Task 5: Based on these services in this file (0-99), create a module which will represets arrival of users (in a fashion) requesting for these services only with all the atrritubes/QoS (bandwith, latency,...ans so on)
Task 4: Allocate the requested RBs by the Users to the nearest BS (check Haochen's codes)')
Task 5: Also indicate that some Users with high prioirty should be allocated to the decicated resource only. Thus indicate in the user repository, what kind of resources that want to be allocated to. 

"""

