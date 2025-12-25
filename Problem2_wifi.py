from typing import List, Set, Tuple
import random
import time
import matplotlib.pyplot as plt


def greedy_wifi_placement(rooms: Set[int], ap_coverage: List[Set[int]]) -> Tuple[List[int], Set[int]]:
    covered: Set[int] = set()
    chosen_aps: List[int] = []

    while covered != rooms:
        best_ap = None
        best_gain = 0

        # Compute gain for each AP
        for i, cov in enumerate(ap_coverage):
            gain = len(cov - covered)
            if gain > best_gain:
                best_gain = gain
                best_ap = i

        # If no AP adds coverage → stop
        if best_gain == 0 or best_ap is None:
            break

        chosen_aps.append(best_ap)
        covered |= ap_coverage[best_ap]

    return chosen_aps, covered

def generate_random_instance(n: int, m: int, coverage_prob: float = 0.2):
    """
    Generate a random Wi-Fi AP placement instance.

    n: number of rooms
    m: number of AP candidates
    coverage_prob: probability a room is covered by any given AP
    """
    rooms = set(range(n))
    ap_coverage = []

    for _ in range(m):
        # Each AP covers each room with probability `coverage_prob`
        coverage = {room for room in rooms if random.random() < coverage_prob}
        ap_coverage.append(coverage)

    return rooms, ap_coverage

def timing_experiment(n_values, m_values, trials=3):
    results = []

    for n in n_values:
        for m in m_values:
            total_time = 0

            for _ in range(trials):
                rooms, ap_cov = generate_random_instance(n, m, coverage_prob=0.2)

                start = time.time()
                greedy_wifi_placement(rooms, ap_cov)
                end = time.time()

                total_time += (end - start)

            avg_time = total_time / trials
            results.append((n, m, avg_time))
            print(f"n={n}, m={m}, time={avg_time:.6f}s")

    return results

def experiment_vary_n(n_values, m=200, trials=3, coverage_prob=0.2):
    results = []

    for n in n_values:
        total_time = 0

        for _ in range(trials):
            rooms, ap_cov = generate_random_instance(n, m, coverage_prob)
            start = time.time()
            greedy_wifi_placement(rooms, ap_cov)
            end = time.time()
            total_time += (end - start)

        avg_time = total_time / trials
        results.append((n, avg_time))
        print(f"n={n}, time={avg_time:.6f}s")

    return results

def plot_results(results):
    # results = list of (n, m, time)
    ms = [m for (_, m, _) in results]
    times = [t for (_, _, t) in results]

    plt.figure(figsize=(8, 5))
    plt.plot(ms, times, marker='o')
    plt.xlabel("Number of APs (m)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Greedy Wi-Fi Algorithm Runtime vs. Number of APs")
    plt.grid(True)
    plt.tight_layout()

def plot_vary_n(results):
    ns = [n for (n, _) in results]
    times = [t for (_, t) in results]

    plt.figure(figsize=(8, 5))
    plt.plot(ns, times, marker='o')
    plt.xlabel("Number of Rooms (n)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime vs. Number of Rooms (n)")
    plt.grid(True)
    plt.tight_layout()
    

def plot_loglog(results):
    ms = [m for (_, m, _) in results]
    times = [t for (_, _, t) in results]

    plt.figure(figsize=(8, 5))
    plt.loglog(ms, times, marker='o', base=10
)
    plt.xlabel("Number of APs (m) [log scale]")
    plt.ylabel("Runtime (seconds) [log scale]")
    plt.title("Log–Log Plot: Runtime vs. Number of APs (m)")
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    


if __name__ == "__main__":
    print("\n=== Experiment 1: Vary m ===")
    n_values = [200]  # Fix number of rooms
    m_values = [50, 100, 150, 200, 250, 300, 400, 500]

    results_m = timing_experiment(n_values, m_values, trials=3)
    plot_results(results_m)
    plot_loglog(results_m)

    print("\n=== Experiment 2: Vary n ===")
    n_values_large = [50, 100, 150, 200, 300, 400, 500, 600]

    results_n = experiment_vary_n(n_values_large, m=200)
    plot_vary_n(results_n)

    plt.show()

