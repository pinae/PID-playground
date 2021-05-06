from datetime import datetime, timedelta
from heater_simulation import HeaterSimulation
from pid import PidDuty
import numpy as np
import pandas as pd
import altair as alt


def make_chart(d):
    data = pd.DataFrame(data={"time": np.concatenate([d["times"], d["times"], d["times"]], axis=0),
                              "value": np.concatenate([d["valve_states"],
                                                       d["liquid_temperatures"],
                                                       d["room_temperatures"]], axis=0),
                              "label": ["valve"] * len(times) + ["water"] * len(times) + ["temperature"] * len(times)})
    chart = alt.Chart(data).mark_line().encode(
        x='time',
        y='value',
        color='label',
        strokeDash='label')
    return chart


if __name__ == "__main__":
    h_sim = HeaterSimulation()
    controller = PidDuty()
    times = np.arange(start=0.5, stop=10*60, step=0.5, dtype=float)
    valve_states = np.empty_like(times)
    liquid_temperatures = np.empty_like(times)
    room_temperatures = np.empty_like(times)
    h_sim.room_temperature = 17.0
    h_sim.liquid_temperature = 17.0
    controller.set_point(20.0)
    now = datetime.now()
    h_sim.last_time = now
    controller.last_time = now
    for i, seconds in enumerate(times):
        time = now + timedelta(seconds=seconds)
        valve = controller.control_loop(measurement=h_sim.room_temperature, time=time)
        h_sim.simulation_step(flow_factor=valve, time=time)
        valve_states[i] = valve
        liquid_temperatures[i] = h_sim.liquid_temperature
        room_temperatures[i] = h_sim.room_temperature
    make_chart({"times": times,
                "valve_states": valve_states,
                "liquid_temperatures": liquid_temperatures,
                "room_temperatures": room_temperatures}).show()
