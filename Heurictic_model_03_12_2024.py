# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 11:31:46 2024

@author: lzr511
"""

"""
Heuristic model: 
    Aim: to dynamically change the ratios of the intra-slice. based on the current environment conditions
    over-here, considering only one slice like URLLC and at some rate the services are coming and cauing the insufficient functionality.
    what we can do is, lets change the ratios of dedicated and prioritization ratio. saying the keeping dedicated ratio quite high and prioritization ratio low.
    This will nake an urgency of making the prioritzation ratio to be higher and thus we shall change its ratio. 
    
    Eventually this can be increased for the other slcies as well. 
    
    
"""

import numpy as np
import matplotlib.pyplot as plt
import random

class Network:
    def __init__(self):
        ###### can make these as non static vars!!!!
        # allocated slices: 'eMBB' = 60%, 'URLLC' = 25%, 'mMTC' = 10%
        self.slice_definitions = {
            'eMBB': {'services': ['Video Streaming', 'File Download'], 'lambda': 5, 'min_prb': 167, 'max_prb': 100},
            'URLLC': {'services': ['Remote Surgery', 'Autonomous Vehicles'], 'lambda': 5, 'min_prb': 70, 'max_prb': 100},
            'mMTC': {'services': ['IoT Monitoring'], 'lambda': 50, 'min_prb': 27, 'max_prb': 100}
        }
        grid_size = 3  # 3x3 grid for base stations
        self.base_stations = [BaseStation(id=i, location=(x, y))
                              for i, (x, y) in enumerate(self.generate_grid_positions(grid_size, spacing=2))]
        lambda_rate = 10
        num_requests = np.random.poisson(lambda_rate)
        print(f"num_requests: {num_requests}")
        
        self.users = []
        for i in range(num_requests):
            # initiate randomised user locations and their prb requests
            user_location = (np.random.uniform(0, 4), np.random.uniform(0, 4))
            prb_randomised = random.choice([15, 9, 60, 41, 3])
            # future work: make any remote surgery ue static by default
            user = User(id=i, type=random.choice(['mobile', 'static']), location=user_location, prb_requested = prb_randomised)
            self.assign_user_to_station(user)
            self.users.append(user)
        #self.users = [User(id=i, type=random.choice(['mobile', 'static']), location=(np.random.uniform(0, 4), np.random.uniform(0, 4))) for i in range(num_requests)]
        
    
    def assign_user_to_station(self, user):
        slice_name = user.determine_slice()
        # ientify nearest station and check if PRBs are available for appropriate network
        nearest_station = min(self.base_stations, key=lambda bs: bs.calculate_distance(user))
        # if nearest_station.does_net_slice_have_prb_space(slice_name, user.prb_requested):
        # print(slice_name, user.prb_requested)
        if nearest_station.can_connect_user_or_standby(user, slice_name):
            user.serving_base_station = nearest_station
            print(user.id, nearest_station.id, True)
        else:
            print(user.id, nearest_station.id, False)
            # print(nearest_station.standby_users)

    def generate_grid_positions(self, size, spacing):
        return [(x, y) for x in np.linspace(0, size - 1, size) * spacing for y in np.linspace(0, size - 1, size) * spacing]

    def simulate_network_operation(self):
        # for slice_name, slice_data in self.slice_definitions.items():
        for user in self.users:
            # print("Here we start: ", user)
            if user.serving_base_station:  # This check is now essentially redundant
                # service_request = random.choice(slice_data['services'])
                snr = user.serving_base_station.calculate_snr(user)
                cqi = user.serving_base_station.calculate_cqi(snr)
                # print(f"User {user.id} ({user.type}) requested {service_request}. SNR: {snr:.2f}, CQI: {cqi}")
                

        self.plot_network()
        
        # Display detailed info for each base station
        for bs in self.base_stations:
            bs.display_base_station_info()
        
        for bs in self.base_stations:
            bs.get_standby_users_info()

    def plot_network(self):
        fig, ax = plt.subplots()
        for bs in self.base_stations:
            ax.plot(bs.location[0], bs.location[1], 'rv', markersize=5)
            ax.text(bs.location[0], bs.location[1], f'{bs.id}({len(bs.connected_users)})', color='red', fontsize=12, ha='right')
        for user in self.users:
            marker = 'bx' if user.type == 'mobile' else 'g*'
            ax.plot(user.location[0], user.location[1], marker, markersize=6)
            ax.text(user.location[0], user.location[1], f'{user.id}', color='blue', fontsize=10, ha='left')

            # Draw a dotted line to the serving base station
            if user.serving_base_station:
                bs = user.serving_base_station
                #print(bs.id)
                ax.plot([user.location[0], bs.location[0]], [user.location[1], bs.location[1]], 'k--', linewidth=1)  # 'k--' is for black dotted line
    
            
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Urban Network Layout')
        plt.grid()
        plt.show()

class BaseStation:
    # ######## !!!!!!!!! make this a non static function
    ########## !!!!!!! check if logistically prb reset works
    ## 167, 70, 27
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.connected_users = []  # List to track connected users
        self.standby_users = [] # List of rejected users due to lack of availabe PRBs
        self.total_prbs = 278  # Number of PRBs available]
        self.available_prb_slices = {
            'eMBB': 167,
            'URLLC': 70,
            'mMTC': 27,        
        }
        
    def can_connect_user_or_standby(self, user, slice_name):
        # function checks if prbs are met and connects the user, otherwise 
        # puts them on standby
        available_prb_for_slice = self.available_prb_slices[slice_name] - user.prb_requested
        if available_prb_for_slice >= 0:
            if user not in self.connected_users:
                self.connected_users.append((user, slice_name))
                self.available_prb_slices[slice_name] = available_prb_for_slice
                return True
        else:
            if user not in self.standby_users:
                self.standby_users.append((user, slice_name))
                return False
    
    def can_connect_standby_user(self, user, slice_name):
        # transfer a standby user to connected user list once prb space has been reshuffled
        was_user_added = self.can_connect_user_or_standby(user, slice_name)
        # delete user from standby list
        if was_user_added:
            if user in self.standby_users:
                indx = self.standby_users.index((user, slice_name))
                self.standby_users.pop(indx)
                return True
            else:
                return False
            
    def can_disconnect_user_to_standby(self, user, slice_name):
        # if user was connected, send it to standby instead
        if user in self.connected_users:
            indx = self.connected_users.index((user, slice_name))
            self.connected_users.pop(indx)
            # add prb back to the available prbs as user goes on standby
            self.update_prb_used_for_slice(slice_name, (-user.prb_request))
            if user not in self.standby_users:
                self.standby_users.append((user, slice_name))
                return True
        return False
            

    def calculate_distance(self, user):
        return np.sqrt((self.location[0] - user.location[0]) ** 2 + (self.location[1] - user.location[1]) ** 2)
        #pass
    
    def does_net_slice_have_prb_space(self, slice_name, prb_requested):
        slice_prb_allowed = self.available_prb_slices[slice_name] - prb_requested
        if slice_prb_allowed >= 0:
            return True
        else:
            return False
    
    def update_prb_used_for_slice(self, slice_name, prb_request):
        # update the slice prbs used if there is space for them
        leftover_prb = self.available_prb_slices[slice_name] - prb_request
        if leftover_prb >= 0:
            self.available_prb_slices[slice_name] = leftover_prb
        else: 
            print("ERROR HAS OCCURRED!!!")

    def calculate_snr(self, user, use_hata=False):
        distance = self.calculate_distance(user)  # distance in meters
        frequency_hz = 2.1e9  # Example frequency for LTE in Hz
        if use_hata:
        # Hata Model for Urban Areas 
            frequency_mhz = frequency_hz / 1e6
            h_bs = 30  # Example base station height in meters
            path_loss_db = 69.55 + 26.16 * np.log10(frequency_mhz) - 13.82 * np.log10(h_bs) + (44.9 - 6.55 * np.log10(h_bs)) * np.log10(distance / 1000)
        
        else:
            # Free Space Path Loss (FSPL)
            c = 3e8  # Speed of light in m/s
            path_loss_db = 20 * np.log10(distance) + 20 * np.log10(frequency_hz) + 20 * np.log10(4 * np.pi / c)

        
        # Using the path loss to calculate received power and SNR
        received_power_dbm = self.transmit_power - path_loss_db
        noise_power_dbm = self.get_noise_power()
        snr = received_power_dbm - noise_power_dbm
        #print(f"snr:{snr}")
            
        return snr

    def calculate_cqi(self, snr):
        #print(f"snr --> {snr}")
        # Adjust CQI mapping to reflect more realistic conditions
        if snr > 20:
            return 15
        elif snr > 15:
            return int(snr - 5)
        elif snr > 10:
            return int(snr - 10)
        else:
            return max(int(snr / 2), 0)

    @property
    def transmit_power(self):
        return 46  # dBm, adjusted for more realistic scenarios

    @property
    def noise_figure(self):
        return 5  # dB

    @property
    def bandwidth(self):
        return 20e6  # Hz

    def get_noise_power(self):
        thermal_noise_dbm_hz = -174
        return thermal_noise_dbm_hz + 10 * np.log10(self.bandwidth) + self.noise_figure
    
    
    def get_connected_users_info(self):
        """ Print information about connected users and their slices """
        for user, slice_name in self.connected_users:
            print(f"    User list: User ID {user.id} on Slice {slice_name}, requested {user.prb_requested}")

    def get_standby_users_info(self):
        """ Print information about connected users and their slices """
        for user, slice_name in self.standby_users:
            print(f"!! The standby Users: User ID {user.id} on Slice {slice_name}, requested {user.prb_requested}")
            print(f"!!   Connection Refused at Base Station {self.id}, PRBs: {self.available_prb_slices[slice_name]}")


    def display_base_station_info(self):
        """ Display information about this base station's load and PRB usage """
        print(f"Base Station {self.id} at Location {self.location}:")
        print(f"  Total Connected Users: {len(self.connected_users)}")
        print(f"  Total PRBs: {self.available_prb_slices}")
        self.get_connected_users_info()

class User:
    def __init__(self, id, type, location, prb_requested):
        self.id = id
        self.type = type
        self.location = location
        self.serving_base_station = None  # Add a reference to the serving base station
        self.prb_requested = prb_requested

    def determine_slice(self):
        """
        Schema for the prbs of each slice and service are assumed as:
        Slice  Service               prb_allocated
        eMBB   Video Streaming       15
        eMBB   File Download         9
        URLLC  Remote Surgery        60
        URLLC  Autonomous Vehicles   41
        mMTC   IoT Monitoring        3
        """
        if self.prb_requested < 5:
            return 'mMTC'
        elif self.prb_requested > 40:
            return 'URLLC'
        
        return 'eMBB'


if __name__ == "__main__":
    # Running the simulation
    network = Network()
    network.simulate_network_operation() 