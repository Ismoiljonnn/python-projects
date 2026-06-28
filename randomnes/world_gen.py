import random
import os

def generate_world():
  user_seed = input("Seed required: ")

  random.seed(user_seed)
  size = 15
  print(f"\ngenerating a world using {user_seed} seed...\n")

  world_map = []
  for y in range(size):
    row = []
    for x in range(size):
      chance = random.random()

      if chance < 0.2:
        tile = "~"
      elif chance < 0.6:
        tile = "."
      elif chance < 0.85:
        tile = "♠"
      else:
        tile = "▲"

      row.append(tile)
    world_map.append(row)

  # for row in world_map:
  #   print(" ".join(row))

  p_x, p_y = 7,7

  hp = 100
  hunger = 100
  inventory = {"berries": 0, "fish": 0}
  current_event = "Welcome to the procedurally generated world!"

  while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 2)

    print("=" * 40)
    print(f"❤️ HP: {hp}/100 | 🍖 Hunger: {hunger}/100 | 🍓 Berries: {inventory['berries']} | 🐟 Fish: {inventory['fish']}")
    print(f"Seed: {user_seed} | Coordinates: ({p_x}, {p_y})")
    print("=" * 40 + "\n")

    print("\n * 2")

    for y in range(size):
      row_display = []
      for x in range(size):
        if x == p_x and y == p_y:
          row_display.append("x")
        else:
          row_display.append(world_map[y][x])
      print(" ".join(row_display))

    current_tile = world_map[p_y][p_x]
    # Unique seed for each tile to lock the event logic
    tile_seed = f"{user_seed}_{p_x}_{p_y}"
    random.seed(tile_seed) 
    
    event_chance = random.random()
    print("-" * 30)
    if current_tile == "~":
        if event_chance < 0.3:
            current_event = "Event: You spotted a terrifying shark! HP -20 🦈"
            hp -= 20
        elif event_chance < 0.7:
            current_event = "Event: You caught a golden fish! Fish +1 🐟"
            inventory["fish"] += 1
        else:
            current_event = "Event: The water is calm, keep swimming. 🌊"
            
    elif current_tile == "♠":
        if event_chance < 0.4:
            current_event = "Event: A wild wolf emerged! HP -15 🐺"
            hp -= 15
        else:
            current_event = "Event: You found some wild berries. Berries +1 🍓"
            inventory["berries"] += 1
            
    elif current_tile == "▲":
        current_event = "Event: The mountain air is freezing! HP -5 🏔️"
        hp -= 5
    else:
        current_event = "Event: The plains are peaceful. No danger here. 🌾"

    print("\n" + "-" * 40)
    print(current_event)

    hunger = max(0, hunger - 5)

    # Agar och qolsa, HP ketadi
    if hunger <= 0:
      current_event += " (You are starving! HP -10 💢)"
      hp -= 10
    print("-" * 40)

    if hp <= 0:
      print("\n💀 YOU DIED! Game Over. 💀")
      break

    print(f"\nCurrent zone: {current_tile}")
    
    move = input("Moving: (w: up, s: down, a: left, d: right, e: eat, q: quit)").lower()

    if move == 'q':
      print("game over")
    elif move == 'e':  # <--- Eat command
      if inventory["berries"] > 0:
        inventory["berries"] -= 1
        hunger = min(100, hunger + 20)
        hp = min(100, hp + 5)
        current_event = "Event: You ate delicious berries! Hunger +20, HP +5 🍓"
      elif inventory["fish"] > 0:
        inventory["fish"] -= 1
        hunger = min(100, hunger + 40)
        hp = min(100, hp + 15)
        current_event = "Event: You cooked and ate a fish! Hunger +40, HP +15 🐟"
      else:
          current_event = "Event: Your inventory is empty! Nothing to eat. 🎒"
    elif move == 'w' and p_y > 0:
      p_y -= 1
    elif move == 's' and p_y < size - 1:
      p_y += 1
    elif move == 'a' and p_x > 0:
      p_x -= 1
    elif move == 'd' and p_x < size - 1:
      p_x += 1


if __name__ == "__main__":
  generate_world()