import json
import os
import sys

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


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Commands: add, log, stats")
    sys.exit()

  cmd = sys.argv[1]
  if cmd == "add":
    add_task(sys.argv[2], sys.argv[3])
  elif cmd == "log":
    log_time(int(sys.argv[2]), int(sys.argv[3]))
  elif cmd == "stats":
    show_stats()