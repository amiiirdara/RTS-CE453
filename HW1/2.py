import copy
import math

print("Executing Non-Preemptive EDF Scheduling...\n")

task_info = [
    {"arrival": 0, "execution": 3, "deadline": 9},
    {"arrival": 1, "execution": 2, "deadline": 6},
    {"arrival": 2, "execution": 1, "deadline": 5},
    {"arrival": 3, "execution": 2, "deadline": 7},
    {"arrival": 0, "execution": 1, "deadline": 4},
]

tasks_edf = copy.deepcopy(task_info)
task_queue = []
current_time = 0
current_task = None
execution_order = []


def log_event(task, current_time, event_type):
    events = {
        "finished": f"[Time {current_time}] Task finished: Arrival={task['arrival']}, Execution={task['execution']}, Deadline={task['deadline']}",
        "queued": f"[Time {current_time}] Task queued: Arrival={task['arrival']}, Execution={task['execution']}, Deadline={task['deadline']}",
        "started": f"[Time {current_time}] Task started: Arrival={task['arrival']}, Execution={task['execution']}, Deadline={task['deadline']}",
    }
    print(events[event_type])


while tasks_edf or task_queue or current_task:
    if (
        current_task
        and current_time == current_task["start"] + current_task["execution"]
    ):
        log_event(current_task, current_time, "finished")
        current_task["completion"] = current_time
        execution_order.append(current_task)
        current_task = None

    for task in tasks_edf[:]:
        if task["arrival"] == current_time:
            log_event(task, current_time, "queued")
            task_queue.append(task)
            tasks_edf.remove(task)

    if not current_task and task_queue:
        task_queue.sort(key=lambda x: x["deadline"])
        current_task = task_queue.pop(0)
        current_task["start"] = current_time
        log_event(current_task, current_time, "started")

    # Increment the current time
    current_time += 1

# Calculate and display the maximum lateness
max_lateness = -math.inf
print("\n--- Task Execution Order ---")
for task in execution_order:
    lateness = task["completion"] - task["deadline"]
    max_lateness = max(max_lateness, lateness)
    print(
        f"Task [Arrival: {task['arrival']}, Execution: {task['execution']}, Deadline: {task['deadline']}]"
    )
    print(
        f"   Start Time: {task['start']}, Completion Time: {task['completion']}, Lateness: {lateness}"
    )
    print("-" * 50)

print(f"\nMaximum Lateness: {max_lateness}")
