from datetime import datetime
from time import time
import random
from pprint import pprint
import matplotlib.pyplot as plt

from src.service.routing_service import find_shortest_paths

random.seed(42)


LOCATIONS = [
    "Warszawa Zachodnia",
    "Warszawa Centralna",
    "Warszawa Bemowo",
    "Pruszków",
    "Otwock",
    "Grodzisk Mazowiecki",
    "Warszawa Rembertów",
    "Warszawa Ursus Niedźwiadek"
]

TIME_SLOTS = [
    (datetime(2026, 1, 1, 8, 0, 0), datetime(2026, 1, 1, 8, 15, 0)),
    (datetime(2026, 1, 1, 8, 0, 0), datetime(2026, 1, 1, 8, 30, 0)),
    (datetime(2026, 1, 1, 8, 0, 0), datetime(2026, 1, 1, 8, 45, 0)),
    (datetime(2026, 1, 1, 8, 0, 0), datetime(2026, 1, 1, 9, 0, 0)),
    (datetime(2026, 1, 1, 8, 0, 0), datetime(2026, 1, 1, 9, 15, 0)),
    (datetime(2026, 1, 1, 8, 0, 0), datetime(2026, 1, 1, 9, 30, 0)),
    (datetime(2026, 1, 1, 8, 0, 0), datetime(2026, 1, 1, 9, 45, 0)),
    (datetime(2026, 1, 1, 8, 0, 0), datetime(2026, 1, 1, 10, 0, 0)),
]


def test_locations():
    print("Testing varying number of end locations")
    times: list[list[float]] = []
    end_locations_count = 1
    while end_locations_count < len(LOCATIONS) - 1:
        print(f"End locations count: {end_locations_count}")
        times.append([])
        i = 0
        for start_location in LOCATIONS:
            print(f"{i + 1}/{len(LOCATIONS)}", end="\r")
            i += 1
            end_locations = random.sample([l for l in LOCATIONS if l != start_location], end_locations_count)
            start = time()
            find_shortest_paths(
                start_location=start_location,
                end_locations=end_locations,
                start_time=datetime(2026, 1, 1, 8, 0, 0),
                end_time=datetime(2026, 1, 1, 8, 15, 0),
            )
            end = time()
            times[end_locations_count - 1].append(end - start)
        end_locations_count += 1
    return times


def test_time_slots():
    print("Testing varying time slots")
    times: list[list[float]] = []
    i = 0
    for start_time, end_time in TIME_SLOTS:
        print(f"Time slot: {start_time} - {end_time}")
        times.append([])
        j = 0
        for start_location in LOCATIONS:
            print(f"{j + 1}/{len(LOCATIONS)}", end="\r")
            j += 1
            end_locations = random.sample([loc for loc in LOCATIONS if loc != start_location], 1)
            start = time()
            find_shortest_paths(
                start_location=start_location,
                end_locations=end_locations,
                start_time=start_time,
                end_time=end_time,
            )
            end = time()
            times[i].append(end - start)
        i += 1
    return times


if __name__ == "__main__":
    print("Starting Dijkstra tests")
    location_times = test_locations()
    pprint(location_times)
    time_slot_times = test_time_slots()
    pprint(time_slot_times)

    loc_avgs = [sum(t) / len(t) for t in location_times]
    time_avgs = [sum(t) / len(t) for t in time_slot_times]

    plt.figure(figsize=(6, 6))
    plt.plot([i + 1 for i in range(len(loc_avgs))], loc_avgs, marker='o')
    plt.title("Average Time vs Number of End Locations")
    plt.xlabel("Number of End Locations")
    plt.ylabel("Average Time (s)")
    plt.savefig("location_times.png")

    plt.clf()

    plt.figure(figsize=(6, 6))
    plt.plot([(i + 1) * 15 for i in range(len(time_avgs))], time_avgs, marker='o')
    plt.title("Average Time vs time range")
    plt.xlabel("Time range (in munutes)")
    plt.ylabel("Average Time (s)")
    plt.savefig("time_slots_times.png")
