
##Tukar this code, this is just an example untuk test rmy code 

from round_robin import PCB, RoundRobinScheduler

processes = [
    PCB("P1", 0, 8),
    PCB("P2", 1, 4),
    PCB("P3", 2, 9),
]

rr = RoundRobinScheduler(processes, quantum=3)
rr.run()
##test simulation
print("Simulation finished\n")

for p in rr.completed:
    print(f"{p.pid}:")
    print(f"  Arrival Time : {p.arrival_time}")
    print(f"  Burst Time   : {p.burst_time}")
    print(f"  Finish Time  : {p.finish_time}")
    print()
