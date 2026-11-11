import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.font.init()

# Window Setup
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stardew Trivia Boss Battles")
clock = pygame.time.Clock()

# Colors
COLOR_BG = (126, 200, 80)
COLOR_SOIL = (109, 76, 65)
COLOR_BORDER = (93, 64, 55)
COLOR_UI_BG = (255, 248, 231)
COLOR_TEXT = (62, 39, 35)
COLOR_BTN = (215, 204, 200)
COLOR_BTN_HOVER = (188, 170, 164)
COLOR_GREEN = (76, 175, 80)
COLOR_RED = (229, 57, 53)
COLOR_GOLD = (255, 235, 59)
COLOR_WHITE = (255, 255, 255)

# Fonts
font_title = pygame.font.SysFont("segoeui", 32, bold=True)
font_text = pygame.font.SysFont("segoeui", 18, bold=True)
font_sub = pygame.font.SysFont("segoeui", 14, bold=True)

# Questions Database
questions_db = [
    {"q": "Which tool is used to till soil for planting?", "options": ["Scythe", "Hoe", "Pickaxe", "Axe"], "answer": 1},
    {"q": "How many days does a season last in Stardew Valley?", "options": ["28 Days", "30 Days", "14 Days", "21 Days"], "answer": 0},
    {"q": "What item restores energy and grows from seeds?", "options": ["Wood", "Crops", "Stone", "Copper"], "answer": 1},
    {"q": "Which tool is used to water dry crops?", "options": ["Watering Can", "Bucket", "Hose", "Sprinkler"], "answer": 0},
    {"q": "What building does Robin construct for animals?", "options": ["Coop", "House", "Silo", "Greenhouse"], "answer": 0},
    {"q": "Which season comes right after Spring?", "options": ["Fall", "Winter", "Summer", "Spring 2"], "answer": 2},
    {"q": "What tool breaks stones and rocks?", "options": ["Hoe", "Pickaxe", "Fishing Rod", "Scythe"], "answer": 1},
    {"q": "What entity sells seeds in town?", "options": ["Willy", "Pierre", "Clint", "Robin"], "answer": 1}
]

# Boss Definitions
bosses = [
    {"name": "Forest Slime King", "max_hp": 100, "color": (76, 175, 80), "scale": 1.0},
    {"name": "Shadow Skeleton", "max_hp": 150, "color": (158, 158, 158), "scale": 1.1},
    {"name": "Ancient Golem", "max_hp": 200, "color": (121, 85, 72), "scale": 1.3}
]

# State Variables
player = {"x": 180.0, "y": 320.0, "target_x": 180.0, "hp": 100, "max_hp": 100}
boss = {"x": 600.0, "y": 300.0, "target_x": 600.0, "hp": 100, "max_hp": 100, "name": "Boss", "color": COLOR_RED, "scale": 1.0}

current_boss_idx = 0
game_state = "MENU"  # MENU, QUIZ, ANIMATING, GAMEOVER
is_player_turn = True
current_q = None
floating_texts = []
overlay_msg = ("Stardew Trivia Boss Battles", "Answer questions correctly to strike monsters and dodge incoming attacks!")
buttons = []

def load_boss(idx):
    b = bosses[idx]
    boss["name"] = b["name"]
    boss["max_hp"] = b["max_hp"]
    boss["hp"] = b["max_hp"]
    boss["color"] = b["color"]
    boss["scale"] = b["scale"]
    boss["x"] = 600.0
    boss["target_x"] = 600.0

def add_floating_text(text, x, y, color):
    floating_texts.append({"text": text, "x": x, "y": y, "color": color, "life": 60})

def setup_quiz():
    global current_q, buttons
    current_q = random.choice(questions_db)
    buttons = []
    
    opt_w, opt_h = 290, 45
    start_x = (WIDTH - (2 * opt_w + 20)) // 2
    start_y = 390
    
    for i, opt in enumerate(current_q["options"]):
        row, col = divmod(i, 2)
        bx = start_x + col * (opt_w + 20)
        by = start_y + row * (opt_h + 10)
        buttons.append({"rect": pygame.Rect(bx, by, opt_w, opt_h), "text": opt, "idx": i})

def handle_answer(selected_idx):
    global game_state, is_player_turn, current_boss_idx
    is_correct = (selected_idx == current_q["answer"])
    game_state = "ANIMATING"
    
    if is_player_turn:
        if is_correct:
            player["target_x"] = boss["x"] - 60
            pygame.time.set_timer(pygame.USEREVENT + 1, 400)
        else:
            boss["target_x"] = boss["x"] + 40
            add_floating_text("BOSS DODGED!", boss["x"], boss["y"] - 40, (180, 180, 180))
            pygame.time.set_timer(pygame.USEREVENT + 2, 500)
    else:
        if is_correct:
            player["target_x"] = player["x"] - 50
            boss["target_x"] = player["x"] + 50
            add_floating_text("DODGED!", player["x"], player["y"] - 40, (129, 199, 132))
            pygame.time.set_timer(pygame.USEREVENT + 2, 500)
        else:
            boss["target_x"] = player["x"] + 50
            pygame.time.set_timer(pygame.USEREVENT + 3, 400)

def start_new_game():
    global current_boss_idx, game_state, is_player_turn
    current_boss_idx = 0
    player["hp"] = player["max_hp"]
    load_boss(current_boss_idx)
    is_player_turn = True
    game_state = "QUIZ"
    setup_quiz()

# Game Loop
running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state in ["MENU", "GAMEOVER"]:
                btn_rect = pygame.Rect(WIDTH//2 - 100, 320, 200, 50)
                if btn_rect.collidepoint(mouse_pos):
                    start_new_game()
            elif game_state == "QUIZ":
                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        handle_answer(btn["idx"])
                        break
                        
        elif event.type == pygame.USEREVENT + 1:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            dmg = 35
            boss["hp"] -= dmg
            add_floating_text(f"-{dmg} CRIT!", boss["x"], boss["y"] - 40, COLOR_GOLD)
            player["target_x"] = 180.0
            
            if boss["hp"] <= 0:
                current_boss_idx += 1
                if current_boss_idx >= len(bosses):
                    game_state = "GAMEOVER"
                    overlay_msg = ("VICTORY!", "You defeated all bosses with your agricultural wisdom!")
                else:
                    load_boss(current_boss_idx)
                    add_floating_text("NEW BOSS ARRIVED!", 400, 200, COLOR_GOLD)
                    is_player_turn = False
                    game_state = "QUIZ"
                    setup_quiz()
            else:
                is_player_turn = False
                game_state = "QUIZ"
                setup_quiz()
                
        elif event.type == pygame.USEREVENT + 2:
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            boss["target_x"] = 600.0
            player["target_x"] = 180.0
            is_player_turn = not is_player_turn
            game_state = "QUIZ"
            setup_quiz()
            
        elif event.type == pygame.USEREVENT + 3:
            pygame.time.set_timer(pygame.USEREVENT + 3, 0)
            dmg = 25
            player["hp"] -= dmg
            add_floating_text(f"-{dmg} HIT!", player["x"], player["y"] - 40, COLOR_RED)
            boss["target_x"] = 600.0
            
            if player["hp"] <= 0:
                game_state = "GAMEOVER"
                overlay_msg = ("DEFEATED!", "The monster overwhelmed you. Try again!")
            else:
                is_player_turn = True
                game_state = "QUIZ"
                setup_quiz()

    # Movement Animation (Smooth Lerp)
    player["x"] += (player["target_x"] - player["x"]) * 0.15
    boss["x"] += (boss["target_x"] - boss["x"]) * 0.15

    # Render Ground & Background
    screen.fill(COLOR_BG)
    pygame.draw.rect(screen, COLOR_SOIL, (50, 340, 700, 100))

    # Render Player
    px, py = int(player["x"]), int(player["y"])
    pygame.draw.rect(screen, (56, 142, 60), (px - 20, py - 40, 40, 50))
    pygame.draw.rect(screen, (255, 204, 128), (px - 15, py - 65, 30, 25))
    pygame.draw.rect(screen, (251, 192, 45), (px - 25, py - 70, 50, 10))

    # Render Boss
    bx, by = int(boss["x"]), int(boss["y"])
    bsize = int(40 * boss["scale"])
    pygame.draw.circle(screen, boss["color"], (bx, by - bsize), bsize)
    pygame.draw.rect(screen, COLOR_WHITE, (bx - bsize//2, by - bsize - 10, 10, 10))
    pygame.draw.rect(screen, COLOR_WHITE, (bx + bsize//4, by - bsize - 10, 10, 10))

    # Render HUD (Health Bars)
    pygame.draw.rect(screen, (0, 0, 0, 150), (10, 10, 220, 40), border_radius=6)
    pygame.draw.rect(screen, (50, 50, 50), (15, 28, 210, 14), border_radius=4)
    p_pct = max(0, player["hp"] / player["max_hp"])
    pygame.draw.rect(screen, COLOR_GREEN, (15, 28, int(210 * p_pct), 14), border_radius=4)
    screen.blit(font_sub.render("Farmer Hero", True, COLOR_WHITE), (15, 12))

    pygame.draw.rect(screen, (0, 0, 0, 150), (WIDTH - 230, 10, 220, 40), border_radius=6)
    pygame.draw.rect(screen, (50, 50, 50), (WIDTH - 225, 28, 210, 14), border_radius=4)
    b_pct = max(0, boss["hp"] / boss["max_hp"])
    pygame.draw.rect(screen, COLOR_RED, (WIDTH - 225, 28, int(210 * b_pct), 14), border_radius=4)
    screen.blit(font_sub.render(boss["name"], True, COLOR_WHITE), (WIDTH - 225, 12))

    # Floating Text Effects
    for ft in floating_texts[:]:
        t_surf = font_text.render(ft["text"], True, ft["color"])
        screen.blit(t_surf, (int(ft["x"] - t_surf.get_width()//2), int(ft["y"])))
        ft["y"] -= 0.8
        ft["life"] -= 1
        if ft["life"] <= 0:
            floating_texts.remove(ft)

    # Quiz Modal Window
    if game_state == "QUIZ" and current_q:
        modal_rect = pygame.Rect(70, 310, 660, 175)
        pygame.draw.rect(screen, COLOR_UI_BG, modal_rect, border_radius=12)
        pygame.draw.rect(screen, COLOR_BORDER, modal_rect, width=4, border_radius=12)
        
        turn_str = "YOUR TURN: Answer to ATTACK!" if is_player_turn else "DEFEND! Answer to DODGE!"
        turn_col = (46, 125, 50) if is_player_turn else (198, 40, 40)
        screen.blit(font_sub.render(turn_str, True, turn_col), (85, 320))
        screen.blit(font_text.render(current_q["q"], True, COLOR_TEXT), (85, 345))
        
        for btn in buttons:
            b_color = COLOR_BTN_HOVER if btn["rect"].collidepoint(mouse_pos) else COLOR_BTN
            pygame.draw.rect(screen, b_color, btn["rect"], border_radius=6)
            pygame.draw.rect(screen, COLOR_BORDER, btn["rect"], width=2, border_radius=6)
            opt_lbl = font_text.render(btn["text"], True, COLOR_TEXT)
            screen.blit(opt_lbl, (btn["rect"].centerx - opt_lbl.get_width()//2, btn["rect"].centery - opt_lbl.get_height()//2))

    # Start / Game Over Overlay
    if game_state in ["MENU", "GAMEOVER"]:
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (0, 0))
        
        t_title = font_title.render(overlay_msg[0], True, COLOR_GOLD)
        t_desc = font_text.render(overlay_msg[1], True, COLOR_WHITE)
        screen.blit(t_title, (WIDTH//2 - t_title.get_width()//2, 180))
        screen.blit(t_desc, (WIDTH//2 - t_desc.get_width()//2, 240))
        
        btn_rect = pygame.Rect(WIDTH//2 - 100, 320, 200, 50)
        btn_col = (102, 187, 106) if btn_rect.collidepoint(mouse_pos) else COLOR_GREEN
        pygame.draw.rect(screen, btn_col, btn_rect, border_radius=8)
        lbl_btn = font_title.render("Start Game" if game_state == "MENU" else "Play Again", True, COLOR_WHITE)
        screen.blit(lbl_btn, (btn_rect.centerx - lbl_btn.get_width()//2, btn_rect.centery - lbl_btn.get_height()//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
