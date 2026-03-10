"""
Connected generators interact more directly and may send data back and forth, often using .send().

Instead of a simple pipeline, they behave more like coroutines communicating.

Visual
Generator A  ◄────►  Generator B
      ▲                 │
      │                 ▼
      └────────► Generator C

Data can flow both directions.
"""


def engine_temp_monitor():
    temp = 0
    while True:
        temp = yield
        if temp > 90:
            print(f"Warning: Engine overheating! Temp = {temp}°C")
        else:
            print(f"Engine temperature is normal: {temp}°C")

# Usage
monitor = engine_temp_monitor()
next(monitor)  # Start the generator

monitor.send(85)  # Engine temperature is normal: 85°C
monitor.send(95)  # Warning: Engine overheating! Temp = 95°C