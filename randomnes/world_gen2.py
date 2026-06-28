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
    pygame.font.init()
    
    # 🖥️ FULL SCREEN SOZLAMASI
    # Ekranning haqiqiy o'lchamlarini aniqlab olamiz
    monitor_info = pygame.display.Info()
    SCREEN_WIDTH = monitor_info.current_w
    SCREEN_HEIGHT = monitor_info.current_h
    
    # UI panel uchun joy ajratamiz, qolgani to'liq xarita bo'ladi
    UI_HEIGHT = 120
    MAP_DISPLAY_HEIGHT = SCREEN_HEIGHT - UI_HEIGHT
    
    # Kataklar o'lchamini ekranga moslab dinamik hisoblaymiz
    TILE_SIZE = min(SCREEN_WIDTH // MAP_SIZE, MAP_DISPLAY_HEIGHT // MAP_SIZE)
    
    # Xaritani markazlashtirish uchun chekka bo'shliqlar (Offset)
    X_OFFSET = (SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)) // 2
    Y_OFFSET = (MAP_DISPLAY_HEIGHT - (MAP_SIZE * TILE_SIZE)) // 2

    # Full screen oynasini ochamiz
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Procedural World UI v3.0 - Full Screen")
    
    font = pygame.font.SysFont("Arial", 24)
    
    # O'yin o'zgaruvchilari
    user_seed = input("Seed required: ")
    world_map = generate_world_data(user_seed)
    p_x, p_y = 7, 7
    hp = 100
    hunger = 100
    inventory = {"berries": 2, "fish": 1} # Sinov uchun boshlang'ich zaxira
    current_event = "Welcome, Ser! Explore using WASD. Press 'E' to eat food."
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                # O'yindan chiqish xavfsizlik tugmasi (Escape)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                moved = False
                # EAT MEXANIKASI (Aktivlashtirildi 🍓/🐟)
                if event.key == pygame.K_e:
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
                
                # Yurish mexanikasi
                elif event.key == pygame.K_w and p_y > 0: p_y -= 1; moved = True
                elif event.key == pygame.K_s and p_y < MAP_SIZE - 1: p_y += 1; moved = True
                elif event.key == pygame.K_a and p_x > 0: p_x -= 1; moved = True
                elif event.key == pygame.K_d and p_x < MAP_SIZE - 1: p_x += 1; moved = True
                
                if moved:
                    hunger = max(0, hunger - 5)
                    starving_msg = " (You are starving! HP -10 💢)" if hunger <= 0 else ""
                    if hunger <= 0: hp -= 10
                    
                    current_tile = world_map[p_y][p_x]
                    tile_seed = f"{user_seed}_{p_x}_{p_y}"
                    random.seed(tile_seed)
                    event_chance = random.random()
                    
                    if current_tile == "~":
                        if event_chance < 0.3: current_event = f"Event: Shark attack! HP -20 🦈{starving_msg}"; hp -= 20
                        elif event_chance < 0.7: current_event = f"Event: Caught a golden fish! Fish +1 🐟{starving_msg}"; inventory["fish"] += 1
                        else: current_event = f"Event: The water is calm. 🌊{starving_msg}"
                    elif current_tile == "♠":
                        if event_chance < 0.4: current_event = f"Event: A wild wolf emerged! HP -15 🐺{starving_msg}"; hp -= 15
                        else: current_event = f"Event: Found some wild berries. Berries +1 🍓{starving_msg}"; inventory["berries"] += 1
                    elif current_tile == "▲": current_event = f"Event: Mountain air is freezing! HP -5 🏔️{starving_msg}"; hp -= 5
                    else: current_event = f"Event: The plains are peaceful. 🌾{starving_msg}"
                    
                    if hp <= 0: current_event = "💀 YOU DIED! Game Over. Press ESC to quit. 💀"

        # Ekranni tozalash (Orqa fon qora)
        screen.fill((0, 0, 0))
        
        # Xaritani markazlashtirilgan offset bilan chizish
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                tile_type = world_map[y][x]
                color = COLORS[tile_type] if not (x == p_x and y == p_y) else COLORS["X"]
                
                pygame.draw.rect(screen, color, (X_OFFSET + x * TILE_SIZE, Y_OFFSET + y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))

        # Dynamic Pastki UI Panel
        pygame.draw.rect(screen, (15, 15, 15), (0, SCREEN_HEIGHT - UI_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))
        
        # Matnlar va inventar holati
        status_text = f"❤️ HP: {hp}/100   |   🍖 Hunger: {hunger}/100   |   🍓 Berries: {inventory['berries']}   |   🐟 Fish: {inventory['fish']}"
        ui_status = font.render(status_text, True, (240, 240, 240))
        ui_event = font.render(current_event, True, (0, 255, 150) if "ate" in current_event or "caught" in current_event else (255, 255, 255))
        ui_control = font.render("Controls: WASD - Move | E - Eat | ESC - Exit", True, (150, 150, 150))
        
        screen.blit(ui_status, (40, SCREEN_HEIGHT - UI_HEIGHT + 20))
        screen.blit(ui_event, (40, SCREEN_HEIGHT - UI_HEIGHT + 55))
        screen.blit(ui_control, (SCREEN_WIDTH - 450, SCREEN_HEIGHT - UI_HEIGHT + 20))

        pygame.display.flip()
        
if __name__ == "__main__":
    main()