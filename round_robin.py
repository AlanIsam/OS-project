from collections import deque
class PCB:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time

        self.start_time = None
        self.finish_time = None

    def __repr__(self):
        return f"{self.pid}(AT={self.arrival_time}, RT={self.remaining_time})"

class ReadyQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, process):
        self.queue.append(process)

    def dequeue(self):
        return self.queue.popleft()

    def is_empty(self):
        return len(self.queue) == 0

class RoundRobinScheduler:
    def __init__(self, processes, quantum, context_switch=1.0):
        self.processes = sorted(processes, key=lambda p: p.arrival_time)
        self.quantum = quantum
        self.context_switch = context_switch

        self.ready_queue = ReadyQueue()
        self.time = 0.0
        self.completed = []

        self.process_index = 0

    def _enqueue_arrivals(self):

        while (
            self.process_index < len(self.processes) and
            self.processes[self.process_index].arrival_time <= self.time
        ):
            self.ready_queue.enqueue(self.processes[self.process_index])
            self.process_index += 1

    def run(self):
        while (
            not self.ready_queue.is_empty() or
            self.process_index < len(self.processes)
        ):

            if self.ready_queue.is_empty():
                self.time = self.processes[self.process_index].arrival_time
                self._enqueue_arrivals()

            current = self.ready_queue.dequeue()

            if current.start_time is None:
                current.start_time = self.time

            run_time = min(self.quantum, current.remaining_time)
            self.time += run_time
            current.remaining_time -= run_time

            self._enqueue_arrivals()

            if current.remaining_time == 0:
                current.finish_time = self.time
                self.completed.append(current)
            else:
                self.ready_queue.enqueue(current)

            if (
                not self.ready_queue.is_empty() or
                self.process_index < len(self.processes)
            ):
                self.time += self.context_switch
