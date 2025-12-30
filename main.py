 
import csv
import random
import copy
from round_robin import PCB, RoundRobinScheduler

def export_process_details(completed_processes, quantum):
    filename = f"details_q{quantum}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["PID", "Arrival", "Burst", "Finish", "TAT", "WT"])
        for p in completed_processes:
            tat = p.finish_time - p.arrival_time
            wt = tat - p.burst_time
            writer.writerow([p.pid, p.arrival_time, p.burst_time, p.finish_time, tat, wt])

def generate_synthetic_processes(count=100):
    """Generates 100 processes based on Design Doc specifications."""
    processes = []
    for i in range(1, count + 1):
        at = random.randint(0, 100) 
        bt = random.randint(5, 50)
        processes.append(PCB(f"P{i}", at, bt))
    return processes

def run_simulations():
    master_list = generate_synthetic_processes()
    quantums = [3, 10, 25]
    summary_data = []

    for q in quantums:
        test_processes = copy.deepcopy(master_list)
        scheduler = RoundRobinScheduler(test_processes, quantum=q)
        scheduler.run()

        export_process_details(scheduler.completed, q)
        
        n = len(scheduler.completed)
        total_tat = sum((p.finish_time - p.arrival_time) for p in scheduler.completed)
        total_wt = sum(((p.finish_time - p.arrival_time) - p.burst_time) for p in scheduler.completed)
        total_overhead = scheduler.context_switches * 1.0
        
        summary_data.append({
            "q": q,
            "atat": total_tat / n,
            "awt": total_wt / n,
            "switches": scheduler.context_switches,
            "overhead": total_overhead
        })

    print("\n" + "="*83)
    print(f"{'Quantum':<10} | {'Avg TAT (ATAT)':<18} | {'Avg Wait (AWT)':<18} | {'Switches':<10} | {'Overhead':<10}")
    print("-" * 83)
    for row in summary_data:
        print(f"{row['q']:<10} | {row['atat']:<18.2f} | {row['awt']:<18.2f} | {row['switches']:<10} | {row['overhead']:<10.1f} ms")
    print("="*83 + "\n")

    with open('simulation_results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=summary_data[0].keys())
        writer.writeheader()
        writer.writerows(summary_data)
    print("Results exported to simulation_results.csv for Performance Analysis.\n")

if __name__ == "__main__":
    run_simulations()
