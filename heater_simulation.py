from datetime import datetime, timedelta


class HeaterSimulation:
    radiator_volume = 5.7 / 1000     # [m³] 1m length 60cm height, type 22 radiator
    liquid_temperature = 30.0        # [°C]
    liquid_thermal_capacity = 4.2    # [kj/(kg*K)] Thermal capacity of water
    liquid_density = 997.0           # [kg/m³] Density of water
    thermal_output = 855.00          # [W] default 855.00W at 55°C supply temperature
    supply_temperature = 55.0        # [°C]
    room_volume = 60                 # [m³]
    room_temperature = 18.0          # [°C]
    max_flow = 0.00000366            # [m³/s]
    radiator_surface_area = 4.07142  # [m²]
    outside_temperature = 10.0       # [°C]
    outside_wall_area = 30.0         # [m³]
    outside_wall_u = 0.17            # [K/W]

    def __init__(self):
        self.last_time = datetime.now()

    def set_thermal_output_by_return_temperature(self, return_temperature, delta_t):
        spread = self.supply_temperature - return_temperature
        self.thermal_output = self.liquid_thermal_capacity * self.radiator_volume * self.liquid_density * spread / (
                delta_t / timedelta(seconds=1))

    def get_return_temperature(self):
        return self.liquid_temperature

    def simulation_step(self, flow_factor=1.0, time=None):
        if time is not None:
            now = time
        else:
            now = datetime.now()
        dt = (now - self.last_time) / timedelta(seconds=1)
        thermal_capacity_air = 1.005  # [kj/(kg*K)]
        density_air = 1.225           # [kg/m³]
        u_radiator = 6.0              # [W/K]
        liquid_exchange_factor = min(flow_factor * self.max_flow * dt / self.radiator_volume, 1.0)
        self.liquid_temperature = (liquid_exchange_factor * self.supply_temperature +
                                   (1.0 - liquid_exchange_factor) * self.liquid_temperature)
        radiator_output = ((self.liquid_temperature - self.room_temperature) * self.radiator_surface_area *
                           u_radiator)
        outside_output = ((self.room_temperature - self.outside_temperature) * self.outside_wall_area *
                          self.outside_wall_u)
        liquid_volume_thermal_capacity = (self.radiator_volume * self.liquid_thermal_capacity *
                                          1000 * self.liquid_density)
        air_thermal_capacity = self.room_volume * thermal_capacity_air * 1000 * density_air
        loss_to_outside = dt * outside_output / air_thermal_capacity
        gain_from_radiator = dt * radiator_output / air_thermal_capacity
        loss_to_radiator = dt * radiator_output / liquid_volume_thermal_capacity
        self.liquid_temperature = self.liquid_temperature - loss_to_radiator
        self.room_temperature = self.room_temperature + gain_from_radiator - loss_to_outside
        self.thermal_output = radiator_output
        return self.room_temperature


if __name__ == "__main__":
    s = HeaterSimulation()
    s.room_temperature = 20.0
    s.liquid_temperature = 55.0
    s.last_time = datetime.now()
    s.simulation_step(flow_factor=0, time=s.last_time + timedelta(seconds=1))
    print(s.thermal_output)
