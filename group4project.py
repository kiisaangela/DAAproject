'''
OKIDI NORBERT           S23B23/051
KIISA ANGELA GRACE      S23B23/027
KISUZE GARETH NEVILLE   S23B23/029
'''


import matplotlib.pyplot as plt
from bisect import bisect_left
import sched
import time

# Task Representation
class Task:
    def __init__(self, name, task_type, deadline, start_time, duration, priority):
        self.name = name
        self.task_type = task_type  # 'personal' or 'academic'
        self.deadline = deadline
        self.start_time = start_time
        self.duration = duration
        self.priority = priority  # Lower value indicates higher priority

    def __repr__(self):
        return (f"{self.name} | {self.task_type} | Deadline: {self.deadline} | "
                f"Start: {self.start_time} | Duration: {self.duration} | Priority: {self.priority}")


# Sorting Tasks
def merge_sort(tasks, key):
    if len(tasks) <= 1:
        return tasks
    mid = len(tasks) // 2
    left = merge_sort(tasks[:mid], key)
    right = merge_sort(tasks[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    sorted_list = []
    while left and right:
        if getattr(left[0], key) <= getattr(right[0], key):
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    sorted_list.extend(left or right)
    return sorted_list


# Searching Tasks
def binary_search(tasks, target_deadline):
    deadlines = [task.deadline for task in tasks]
    index = bisect_left(deadlines, target_deadline)
    if index < len(tasks) and deadlines[index] == target_deadline:
        return tasks[index]
    return None


# Dynamic Programming for Scheduling
def maximize_tasks(tasks):
    tasks = merge_sort(tasks, 'deadline')
    dp = [0] * len(tasks)
    dp[0] = tasks[0].duration
    for i in range(1, len(tasks)):
        include_task = tasks[i].duration
        last_non_conflicting = -1
        for j in range(i - 1, -1, -1):
            if tasks[j].deadline <= tasks[i].start_time:
                last_non_conflicting = j
                break
        if last_non_conflicting != -1:
            include_task += dp[last_non_conflicting]
        dp[i] = max(include_task, dp[i - 1])
    return dp[-1]


# Visualization: Gantt Chart
def plot_gantt(tasks):
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, task in enumerate(tasks):
        ax.barh(task.name, task.duration, left=task.start_time,
                color='skyblue' if task.task_type == 'personal' else 'orange')
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    ax.set_title('Task Schedule Gantt Chart')
    plt.show()


# Reminder System
scheduler = sched.scheduler(time.time, time.sleep)

def schedule_reminder(task):
    delay = max(0, (task.deadline - time.time()))
    scheduler.enter(delay, 1, print, argument=(f"Reminder: {task.name} is due!",))


# Example
if __name__ == "__main__":
    # Sample Tasks
    tasks = [
        Task("Study OOP", "academic", deadline=10, start_time=2, duration=3, priority=1),
        Task("Gym", "personal", deadline=15, start_time=12, duration=2, priority=2),
        Task("Complete Assignment", "academic", deadline=20, start_time=16, duration=4, priority=1),
        Task("Grocery Shopping", "personal", deadline=8, start_time=1, duration=1, priority=3)
    ]

    # Sorting Tasks by Priority
    tasks = merge_sort(tasks, key='priority')
    print("Tasks Sorted by Priority:")
    for task in tasks:
        print(task)

    # Binary Search for a Task with a Specific Deadline
    print("\nSearching for a Task with Deadline 15:")
    found_task = binary_search(tasks, 15)
    print(found_task if found_task else "No task found with this deadline.")

    # Maximize Task Completion using DP
    print("\nMaximum Task Duration Achievable:")
    print(maximize_tasks(tasks))

    # Plot Gantt Chart
    print("\nVisualizing Gantt Chart...")
    plot_gantt(tasks)

    # Schedule Reminders
    print("\nScheduling Reminders...")
    for task in tasks:
        schedule_reminder(task)

    print("Running Reminders...")
    scheduler.run()
