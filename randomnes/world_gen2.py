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
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Procedural World UI")
    
    user_seed = input("Seed required: ")
    world_map = generate_world_data(user_seed)
    
    p_x, p_y = 7, 7 # Boshlang'ich pozitsiya
    
    # O'yinning asosiy sikli
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Tugmalar bosilishini tekshirish
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and p_y > 0: p_y -= 1
                elif event.key == pygame.K_s and p_y < MAP_SIZE - 1: p_y += 1
                elif event.key == pygame.K_a and p_x > 0: p_x -= 1
                elif event.key == pygame.K_d and p_x < MAP_SIZE - 1: p_x += 1

        # Xaritani qayta chizish
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                tile_type = world_map[y][x]
                color = COLORS[tile_type]
                
                # Agar bu katakda o'yinchi turgan bo'lsa
                if x == p_x and y == p_y:
                    color = COLORS["X"]
                    
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()

if __name__ == "__main__":
    main()