import random

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
  inventory = {"berries": 0, "fish": 0}
  current_event = "Welcome to the procedurally generated world!"

  while True:
    print("\n" * 5)

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
    if current_tile == "~": # Water
        if event_chance < 0.3:
            print("Event: You spotted a terrifying shark! 🦈")
        elif event_chance < 0.7:
            print("Event: You caught a golden fish! 🐟")
        else:
            print("Event: The water is calm, keep swimming. 🌊")
            
    elif current_tile == "♠": # Forest
        if event_chance < 0.4:
            print("Event: A wild wolf emerged from behind the trees! 🐺")
        else:
            print("Event: You found a bunch of wild berries. 🍓")
            
    elif current_tile == "▲": # Mountain
        print("Event: The mountain air is freezing, stay cautious! 🏔️")
    else: # Plains
        print("Event: The plains are peaceful. No danger here. 🌾")
    print("-" * 30)

    print(f"\nCurrent zone: {current_tile}")
    
    move = input("Moving: (w: up, s: down, a: left, d: right, q: quit)").lower()

    if move == 'q':
      print("game over")
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