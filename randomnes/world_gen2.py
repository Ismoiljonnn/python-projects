import pygame
import random
import sys

# O'yin oynasi o'lchamlari (Boshlang'ich va xarita o'lchamlari)
MAP_SIZE = 15

# Ranglar palitrasi
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

def get_seed_from_ui():
    """Grafik oynada foydalanuvchidan seed matnini qabul qiluvchi funksiya"""
    pygame.init()
    pygame.font.init()
    
    # Boshlang'ich menyu oynasi o'lchami
    menu_width, menu_height = 600, 400
    screen = pygame.display.set_mode((menu_width, menu_height))
    pygame.display.set_caption("Enter Seed to Begin Strategy")
    
    font_large = pygame.font.SysFont("Arial", 32, bold=True)
    font_small = pygame.font.SysFont("Arial", 24)
    
    user_seed = ""
    menu_running = True
    
    while menu_running:
        screen.fill((20, 20, 25)) # To'q fon
        
        # UI Matnlari
        title_surf = font_large.render("PROCEDURAL WORLD GENERATOR", True, (0, 255, 150))
        prompt_surf = font_small.render("Enter Seed text and press ENTER:", True, (200, 200, 200))
        
        # Kiritilayotgan matn qutisi (box)
        pygame.draw.rect(screen, (40, 40, 50), (100, 200, 400, 50), border_radius=5)
        seed_surf = font_small.render(user_seed + "|", True, (255, 255, 255))
        
        # Chizish koordinatalari
        screen.blit(title_surf, ((menu_width - title_surf.get_width()) // 2, 60))
        screen.blit(prompt_surf, (100, 160))
        screen.blit(seed_surf, (115, 212))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN: # Enter bosilganda
                    if user_seed.strip() != "":
                        menu_running = False
                elif event.key == pygame.K_BACKSPACE: # O'chirish
                    user_seed = user_seed[:-1]
                else:
                    # Faqat harflar va sonlarni qabul qilish
                    if len(user_seed) < 15 and event.unicode.isprintable():
                        user_seed += event.unicode
                        
    return user_seed

def main():
    # 🌟 1-QADAM: Birinchi UI orqali Seed so'raymiz
    user_seed = get_seed_from_ui()
    
    # 🌟 2-QADAM: Monitor o'lchamlarini olib Full Screen-ga o'tamiz
    monitor_info = pygame.display.Info()
    SCREEN_WIDTH = monitor_info.current_w
    SCREEN_HEIGHT = monitor_info.current_h
    
    UI_HEIGHT = 120
    MAP_DISPLAY_HEIGHT = SCREEN_HEIGHT - UI_HEIGHT
    
    TILE_SIZE = min(SCREEN_WIDTH // MAP_SIZE, MAP_DISPLAY_HEIGHT // MAP_SIZE)
    X_OFFSET = (SCREEN_WIDTH - (MAP_SIZE * TILE_SIZE)) // 2
    Y_OFFSET = (MAP_DISPLAY_HEIGHT - (MAP_SIZE * TILE_SIZE)) // 2

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Procedural World UI v3.0 - Full Screen")
    
    font = pygame.font.SysFont("Arial", 24)
    symbol_font = pygame.font.SysFont("Arial", int(TILE_SIZE * 0.4), bold=True)
    
    # O'yin o'zgaruvchilari
    world_map = generate_world_data(user_seed)
    p_x, p_y = 7, 7
    hp = 100
    hunger = 100
    inventory = {"berries": 2, "fish": 1}
    current_event = f"Welcome, Ser! Seed '{user_seed}' applied. Explore using WASD."
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                moved = False
                # EAT MEXANIKASI
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

        screen.fill((0, 0, 0))
        
        # Xaritani simvollar bilan chizish
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                tile_type = world_map[y][x]
                is_player = (x == p_x and y == p_y)
                
                color = COLORS[tile_type] if not is_player else COLORS["X"]
                rect_coords = (X_OFFSET + x * TILE_SIZE, Y_OFFSET + y * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1)
                
                pygame.draw.rect(screen, color, rect_coords)

                # Katak simvollari (Tushunarli qilish uchun)
                if is_player:
                    char, char_color = "P", (255, 255, 255)
                elif tile_type == "~":
                    char, char_color = "W", (15, 60, 100)
                elif tile_type == ".":
                    char, char_color = "L", (140, 110, 70)
                elif tile_type == "♠":
                    char, char_color = "F", (10, 70, 10)
                elif tile_type == "▲":
                    char, char_color = "M", (50, 60, 70)
                
                char_surface = symbol_font.render(char, True, char_color)
                text_x = X_OFFSET + x * TILE_SIZE + (TILE_SIZE - char_surface.get_width()) // 2
                text_y = Y_OFFSET + y * TILE_SIZE + (TILE_SIZE - char_surface.get_height()) // 2
                screen.blit(char_surface, (text_x, text_y))

        # Dynamic Pastki UI Panel
        pygame.draw.rect(screen, (15, 15, 15), (0, SCREEN_HEIGHT - UI_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))
        
        status_text = f"❤️ HP: {hp}/100   |   🍖 Hunger: {hunger}/100   |   🍓 Berries: {inventory['berries']}   |   🐟 Fish: {inventory['fish']}"
        ui_status = font.render(status_text, True, (240, 240, 240))
        ui_event = font.render(current_event, True, (0, 255, 150) if "ate" in current_event or "caught" in current_event else (255, 255, 255))
        ui_control = font.render(f"Seed: {user_seed} | WASD - Move | E - Eat | ESC - Exit", True, (150, 150, 150))
        
        screen.blit(ui_status, (40, SCREEN_HEIGHT - UI_HEIGHT + 20))
        screen.blit(ui_event, (40, SCREEN_HEIGHT - UI_HEIGHT + 55))
        screen.blit(ui_control, (SCREEN_WIDTH - 500, SCREEN_HEIGHT - UI_HEIGHT + 20))

        pygame.display.flip()

if __name__ == "__main__":
    main()