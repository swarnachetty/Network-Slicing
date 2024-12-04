import numpy as np
import matplotlib.pyplot as plt
import random

class Network:
    def __init__(self):
        grid_size = 3  # 3x3 grid for base stations
        self.base_stations = [BaseStation(id=i, location=(x, y))
                              for i, (x, y) in enumerate(self.generate_grid_positions(grid_size, spacing=1))]
        self.users = [User(id=i, type=random.choice(['mobile', 'static']), location=(np.random.uniform(0, 3), np.random.uniform(0, 3))) for i in range(100)]
        self.slice_definitions = {
            'eMBB': {'services': ['Video Streaming', 'File Download'], 'lambda': 80},
            'URLLC': {'services': ['Remote Surgery', 'Autonomous Vehicles'], 'lambda': 30},
            'mMTC': {'services': ['IoT Monitoring'], 'lambda': 50}
        }

    def generate_grid_positions(self, size, spacing):
        return [(x, y) for x in np.linspace(0, size - 1, size) * spacing for y in np.linspace(0, size - 1, size) * spacing]

    def simulate_network_operation(self):
        for slice_name, slice_data in self.slice_definitions.items():
            num_requests = np.random.poisson(slice_data['lambda'])
            #print(f"slice_name: {slice_name} --> {num_requests}")
            for _ in range(num_requests):
                user = random.choice(self.users)
                service_request = random.choice(slice_data['services'])
                serving_base_station = min(self.base_stations, key=lambda bs: bs.calculate_distance(user))
                snr = serving_base_station.calculate_snr(user)
                cqi = serving_base_station.calculate_cqi(snr)
                print(f"slice_name: {slice_name} --> {_} --> {cqi}")
                #print(f"Slice {slice_name}: User {user.id} ({user.type}) at {user.location} requested {service_request} from Base Station {serving_base_station.id} at {serving_base_station.location}. SNR: {snr:.2f}, CQI: {cqi}")
        self.plot_network()

    def plot_network(self):
        fig, ax = plt.subplots()
        for bs in self.base_stations:
            ax.plot(bs.location[0], bs.location[1], 'ro', markersize=10)
        for user in self.users:
            marker = 'bx' if user.type == 'mobile' else 'gx'
            ax.plot(user.location[0], user.location[1], marker, markersize=5)
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Urban Network Layout')
        plt.show()

class BaseStation:
    def __init__(self, id, location):
        self.id = id
        self.location = location

    def calculate_distance(self, user):
        return np.sqrt((self.location[0] - user.location[0]) ** 2 + (self.location[1] - user.location[1]) ** 2)

    def calculate_snr(self, user):
        distance = self.calculate_distance(user)
        print(distance)
        path_loss_exponent = 3.5
        # Introduce more variability and realistic transmission power settings
        received_power = self.transmit_power - 10 * path_loss_exponent * np.log10(distance + 0.1) - random.uniform(0, 10)
        noise_power = self.get_noise_power()
        snr = received_power - noise_power
        print(f"received_power: {received_power}")
        return received_power - noise_power

    def calculate_cqi(self, snr):
        print(f"snr --> {snr}")
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

class User:
    def __init__(self, id, type, location):
        self.id = id
        self.type = type
        self.location = location

# Running the simulation
network = Network()
network.simulate_network_operation() 