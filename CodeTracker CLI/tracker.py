import json
import os

DB_FILE = "data.json"

def load_data():
  if not os.path.exists(DB_FILE):
    return {"tasks": []}
  with open(DB_FILE, "r") as f:
    return json.load(f)

def save_data(data):
  with open(DB_FILE, "w") as f:
    json.jump(data, f, indent=4)


def add_task(name, category):
  data = load_data()
  new_task = {
    "id": len(data["tasks"]) + 1,
    "name": name,
    "category": category,
    "total_minutes": 0
  }
  data["tasks"].append(new_task)
  save_data(data)
  print(f"-> Task '{name}' added.")

def log_time(task_id, minutes):
  data = load_data()
  for task in data["tasks"]:
    if task["id"] == task_id:
      task["total_minutes"] += minutes
      save_data(data)
      print(f"-> {minutes} minutes added to {task['name']}.")
      return
    print("-> Task coldn't find!")

def show_stats():
  data = load_data()
  print("\n=== Progress report ===")
  for task in data["tasks"]:
    print(f"[{task['id']}] {task['name']} ({task['category']}) - {task['total_minutes']} min")