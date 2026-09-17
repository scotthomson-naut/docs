from zoho_tasks import find_task

task = find_task(
    "There are no Uvs on any objects",
    tasklist="UVs"
)

if task:
    print("Prefix:", task.get("prefix"))
    print("API ID:", task.get("id"))
else:
    print("Task not found")