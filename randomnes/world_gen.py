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

  for row in world_map:
    print(" ".join(row))


if __name__ == "__main__":
  generate_world()