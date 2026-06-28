import pygame
import random
import sys

# O'yin oynasi o'lchamlari
TILE_SIZE = 40
MAP_SIZE = 15
MAP_HEIGHT = TILE_SIZE * MAP_SIZE  # 600 piksel xarita uchun
UI_HEIGHT = 100                    # 100 piksel matnlar uchun pastki panel
SCREEN_WIDTH = TILE_SIZE * MAP_SIZE
SCREEN_HEIGHT = MAP_HEIGHT + UI_HEIGHT

# Ranglar palitrasi (Hozircha rasmlar o'rniga ranglar bilan chizamiz)
COLORS = {
    "~": (28, 107, 160),   # Moviy suv
    ".": (214, 185, 141),  # Qumloq yer
    "♠": (34, 139, 34),    # To'q yashil o'rmon
    "▲": (112, 128, 144),  # Kulrang tog'
    "X": (220, 20, 60)     # Qizil qahramon
}

def generate_world_data(seed_val):
    random.seed(seed_val)
    world_map = []
    for y in range(MAP_SIZE):
        row = []
        for x in range(MAP_SIZE):
            chance = random.random()
            if chance < 0.2: tile = "~"
            elif chance < 0.6: tile = "."
            elif chance < 0.85: tile = "♠"
            else: tile = "▲"
            row.append(tile)
        world_map.append(row)
    return world_map

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Procedural World UI v2.0")
    
    # Shrift tizimini yoqish
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 20)
    
    user_seed = input("Seed required: ")
    world_map = generate_world_data(user_seed)
    
    p_x, p_y = 7, 7
    
    hp = 100
    hunger = 100
    inventory = {"berries": 0, "fish": 0}
    current_event = "Welcome to the procedurally generated world!"
    size = MAP_SIZE  # xarita o'lchami sharti uchun
    
    # O'yinning asosiy sikli
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Tugmalar bosilishini tekshirish
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_w and p_y > 0: 
                    p_y -= 1
                    moved = True
                elif event.key == pygame.K_s and p_y < MAP_SIZE - 1: 
                    p_y += 1
                    moved = True
                elif event.key == pygame.K_a and p_x > 0: 
                    p_x -= 1
                    moved = True
                elif event.key == pygame.K_d and p_x < MAP_SIZE - 1: 
                    p_x += 1
                    moved = True
                
                # Agar o'yinchi haqiqatdan ham qadam bosgan bo'lsa
                if moved:
                    hunger = max(0, hunger - 5)
                    if hunger <= 0:
                        hp -= 10
                        starving_msg = " (You are starving! HP -10 💢)"
                    else:
                        starving_msg = ""

                    # Tile seed va voqea mantig'i (Terminal kodingizdan olindi)
                    current_tile = world_map[p_y][p_x]
                    tile_seed = f"{user_seed}_{p_x}_{p_y}"
                    random.seed(tile_seed)
                    event_chance = random.random()

                    if current_tile == "~":
                        if event_chance < 0.3:
                            current_event = f"Event: You spotted a terrifying shark! HP -20 🦈{starving_msg}"
                            hp -= 20
                        elif event_chance < 0.7:
                            current_event = f"Event: You caught a golden fish! Fish +1 🐟{starving_msg}"
                            inventory["fish"] += 1
                        else:
                            current_event = f"Event: The water is calm. 🌊{starving_msg}"
                    elif current_tile == "♠":
                        if event_chance < 0.4:
                            current_event = f"Event: A wild wolf emerged! HP -15 🐺{starving_msg}"
                            hp -= 15
                        else:
                            current_event = f"Event: You found some wild berries. Berries +1 🍓{starving_msg}"
                            inventory["berries"] += 1
                    elif current_tile == "▲":
                        current_event = f"Event: The mountain air is freezing! HP -5 🏔️{starving_msg}"
                        hp -= 5
                    else:
                        current_event = f"Event: The plains are peaceful. 🌾{starving_msg}"
                    
                    # HP nolga tushsa o'yinni to'xtatish sharti
                    if hp <= 0:
                        current_event = "💀 YOU DIED! Game Over. 💀"

        # Xaritani qayta chizish
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                tile_type = world_map[y][x]
                color = COLORS[tile_type]
                
                # Agar bu katakda o'yinchi turgan bo'lsa
                if x == p_x and y == p_y:
                    color = COLORS["X"]
                    
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # Pastki UI panel uchun qora to'rtburchak chizish
        pygame.draw.rect(screen, (0, 0, 0), (0, MAP_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))
        
        # Terminaldagi mantiq asosida matnlarni tayyorlash
        hp_text = font.render(f"HP: {hp}/100", True, (255, 50, 50))       # Qizil matn
        hunger_text = font.render(f"Hunger: {hunger}/100", True, (255, 165, 0)) # To'q sariq
        event_text = font.render(current_event, True, (255, 255, 255))    # Oq matn
        
        # Matnlarni ekrandagi koordinatalariga joylashtirish
        screen.blit(hp_text, (20, MAP_HEIGHT + 15))
        screen.blit(hunger_text, (180, MAP_HEIGHT + 15))
        screen.blit(event_text, (20, MAP_HEIGHT + 50))

        pygame.display.flip()

if __name__ == "__main__":
    main()