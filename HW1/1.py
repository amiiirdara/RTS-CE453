import copy
import math
from collections import deque

def run_bratley_algorithm():
    print("Executing Bratley Algorithm:\n")
    tasks_data = [
        {'arrival': 0, 'execution': 3, 'deadline': 9, 'start': None, 'completion': None, 'prev_task': None},
        {'arrival': 1, 'execution': 2, 'deadline': 6, 'start': None, 'completion': None, 'prev_task': None},
        {'arrival': 2, 'execution': 1, 'deadline': 5, 'start': None, 'completion': None, 'prev_task': None},
        {'arrival': 3, 'execution': 2, 'deadline': 7, 'start': None, 'completion': None, 'prev_task': None},
        {'arrival': 0, 'execution': 1, 'deadline': 4, 'start': None, 'completion': None, 'prev_task': None}
    ]

    feasible_solutions = []
    initial_state = {'task_list': tasks_data, 'current_task': None}
    queue = deque([initial_state])

    while queue:
        state = queue.popleft()
        remaining_tasks = state['task_list']
        current_task = state['current_task']

        if not remaining_tasks:
            task_sequence = []
            task = current_task
            while task:
                task_sequence.append(task)
                task = task.get('prev_task')
            task_sequence.reverse()
            
            print("Task Sequence:")
            for task in task_sequence:
                print(f"  Task: [Arrival: {task['arrival']}, Execution: {task['execution']}, Deadline: {task['deadline']}]")
                print(f"         Start: {task['start']}, Completion: {task['completion']}")
            print("  --> Sequence is Feasible")
            print("----------------------------------------------------------")
            
            feasible_solutions.append(current_task)
            continue

        for index in range(len(remaining_tasks)):
            task_copy = copy.deepcopy(remaining_tasks)
            task_candidate = task_copy.pop(index)
            if current_task is None:
                task_candidate['start'] = task_candidate['arrival']
                task_candidate['completion'] = task_candidate['arrival'] + task_candidate['execution']
            else:
                task_candidate['prev_task'] = current_task
                task_candidate['start'] = max(task_candidate['arrival'], current_task['completion'])
                task_candidate['completion'] = task_candidate['start'] + task_candidate['execution']

            if task_candidate['completion'] > task_candidate['deadline']:
                task_sequence = []
                task = task_candidate
                while task:
                    task_sequence.append(task)
                    task = task.get('prev_task')
                task_sequence.reverse()
                
                print("Task Sequence:")
                for task in task_sequence:
                    print(f"  Task: [Arrival: {task['arrival']}, Execution: {task['execution']}, Deadline: {task['deadline']}]")
                    print(f"         Start: {task['start']}, Completion: {task['completion']}")
                print("  --> Sequence is Infeasible")
                print("----------------------------------------------------------")
                
                continue

            new_state = {'task_list': task_copy, 'current_task': task_candidate}
            queue.append(new_state)

    solution_sequence = []
    task = feasible_solutions[0]
    while task:
        solution_sequence.append(task)
        task = task.get('prev_task')
    solution_sequence.reverse()

    max_lateness = -math.inf
    print("\nFinal Schedule:")
    for task in solution_sequence:
        lateness = task['completion'] - task['deadline']
        max_lateness = max(max_lateness, lateness)
        print(f"Task: [Arrival: {task['arrival']}, Execution: {task['execution']}, Deadline: {task['deadline']}]")
        print(f"       Start: {task['start']}, Completion: {task['completion']}, Lateness: {lateness}")

    print(f"\nMaximum Lateness: {max_lateness}")



if __name__ == "__main__":
    run_bratley_algorithm()
