import pygame
import random
import sys
import math

pygame.init()
WIDTH, HEIGHT = 1400, 870
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (100, 150, 255)
ORANGE = (255, 165, 0)
PURPLE = (160, 32, 240)
GOLD = (255, 215, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
DARKER_BROWN = (61, 37, 13)
SKIN = (255, 200, 150)
DARK_GREEN = (0, 100, 0)
APPLE_RED = (255, 0, 0)
APPLE_POINTS = 250

PLAYER_SPEED = 12.5
ENEMY_SPEED = 2.5
ENEMY_SPAWN_TIME = 1000

DIFFICULTY_SETTINGS = {
    "easy": {
        "player_speed": 15,
        "enemy_speed": 1.5,
        "enemy_spawn_time": 2000,
        "enemy_hp": 30,
        "enemy_damage": 2,
        "color": BROWN,
        "desc": "Медленные враги, очень просто"
    },
    "normal": {
        "player_speed": 12.5,
        "enemy_speed": 2.5,
        "enemy_spawn_time": 2000,
        "enemy_hp": 50,
        "enemy_damage": 2,
        "color": BROWN,
        "desc": "Сбалансировано"
    },
    "hard": {
        "player_speed": 10,
        "enemy_speed": 3.5,
        "enemy_spawn_time": 2000,
        "enemy_hp": 70,
        "enemy_damage": 2,
        "color": DARK_BROWN,
        "desc": "Быстрые враги, сложно"
    },
    "hardcore": {
        "player_speed": 10,
        "enemy_speed": 5,
        "enemy_spawn_time": 2000,
        "enemy_hp": 100,
        "enemy_damage": 2,
        "color": DARKER_BROWN,
        "desc": "Очень быстро и сложно"
    }
}

class Button:
    def __init__(self, x, y, w, h, text, color=LIGHT_BLUE, text_color=BLACK, font_size=32):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False
        self.font_size = font_size

    def draw(self, surface, font):
        color = self.color
        if self.hovered:
            color = (min(self.color[0] + 40, 255), min(self.color[1] + 40, 255), min(self.color[2] + 40, 255))
            pygame.draw.rect(surface, GOLD, self.rect.inflate(8, 8), border_radius=18, width=4)
        shadow_rect = self.rect.inflate(4, 4)
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=15)
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=15)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Unit:
    def __init__(self, x, y, color, hp=100, speed=5, damage=10):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.color = color
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.damage = damage
        self.alive = True

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def attack(self, target):
        target.take_damage(self.damage)

class Player(Unit):
    def __init__(self, x, y, color, hp=100, speed=5, damage=10):
        super().__init__(x, y, color, hp, speed, damage)
        self.animation_offset = 0
        self.animation_direction = 1

    def draw(self, surface):
        self.animation_offset += 0.1 * self.animation_direction
        if self.animation_offset > 2 or self.animation_offset < -2:
            self.animation_direction *= -1

        body_rect = self.rect.inflate(-6, -6)
        pygame.draw.rect(surface, DARK_GREEN, self.rect, border_radius=8)
        pygame.draw.rect(surface, GREEN, body_rect, border_radius=6)

        belt_y = self.rect.y + 35
        pygame.draw.rect(surface, RED, (self.rect.x + 5, belt_y, 30, 6), border_radius=2)
        pygame.draw.rect(surface, (200, 0, 0), (self.rect.x + 7, belt_y + 1, 26, 4), border_radius=2)

        for i in range(2):
            line_y = self.rect.y + 20 + i * 12
            pygame.draw.line(surface, DARK_GREEN, (self.rect.x + 8, line_y), (self.rect.x + 32, line_y), 2)

        head_center = (self.rect.centerx, self.rect.y - 8 + self.animation_offset)
        pygame.draw.circle(surface, SKIN, head_center, 12)
        pygame.draw.circle(surface, (230, 180, 130), head_center, 10)

        pygame.draw.rect(surface, BLACK, (head_center[0] - 12, head_center[1] - 10, 24, 8), border_radius=4)
        pygame.draw.line(surface, RED, (head_center[0] - 8, head_center[1] - 6), (head_center[0] + 8, head_center[1] - 6), 3)

        pygame.draw.circle(surface, WHITE, (head_center[0] - 4, head_center[1] - 1), 3)
        pygame.draw.circle(surface, WHITE, (head_center[0] + 4, head_center[1] - 1), 3)
        pygame.draw.circle(surface, BLACK, (head_center[0] - 3, head_center[1] - 2), 2)
        pygame.draw.circle(surface, BLACK, (head_center[0] + 5, head_center[1] - 2), 2)

        mask = pygame.Rect(head_center[0] - 7, head_center[1] + 3, 14, 5)
        pygame.draw.rect(surface, DARK_GREEN, mask, border_radius=2)

        sword_x = self.rect.right - 6
        sword_y = self.rect.y + 25
        pygame.draw.line(surface, GRAY, (sword_x, sword_y), (sword_x + 20, sword_y - 5), 3)
        pygame.draw.line(surface, (139, 69, 19), (sword_x - 3, sword_y), (sword_x, sword_y), 2)

        pygame.draw.rect(surface, GREEN, (self.rect.x - 4, self.rect.y + 15, 6, 20), border_radius=3)
        pygame.draw.rect(surface, GREEN, (self.rect.right - 2, self.rect.y + 15, 6, 20), border_radius=3)

        pygame.draw.rect(surface, DARK_GREEN, (self.rect.x + 6, self.rect.bottom - 15, 8, 18), border_radius=3)
        pygame.draw.rect(surface, DARK_GREEN, (self.rect.x + 26, self.rect.bottom - 15, 8, 18), border_radius=3)

        if self.hp < self.max_hp:
            bar_width = 40
            bar_height = 5
            bar_x = self.rect.x
            bar_y = self.rect.y - 10
            pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height))
            fill_width = int((self.hp / self.max_hp) * bar_width)
            pygame.draw.rect(surface, GREEN, (bar_x, bar_y, fill_width, bar_height))

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)

class Enemy(Unit):
    def __init__(self, x, y, color, hp=100, speed=5, damage=10):
        super().__init__(x, y, color, hp, speed, damage)
        self.animation_offset = random.uniform(0, 6.28)

    def draw(self, surface):
        self.animation_offset += 0.05

        points = []
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            r = 18 + math.sin(self.animation_offset) * 2
            x = self.rect.centerx + math.cos(rad) * r
            y = self.rect.centery + math.sin(rad) * r - 5
            points.append((x, y))
        pygame.draw.polygon(surface, self.color, points)

        for i in range(4):
            spike_x = self.rect.right - 8 + i * 6
            spike_y = self.rect.y + 10 + i * 12
            pygame.draw.polygon(surface, DARKER_BROWN, [(spike_x, spike_y), (spike_x + 8, spike_y - 6), (spike_x + 4, spike_y + 4)])

        for _ in range(6):
            cx = self.rect.x + random.randint(8, 32)
            cy = self.rect.y + random.randint(8, 52)
            pygame.draw.line(surface, DARKER_BROWN, (cx, cy), (cx + random.randint(-4, 4), cy + random.randint(-4, 4)), 2)

        eye_l = (self.rect.centerx - 10, self.rect.y + 15)
        eye_r = (self.rect.centerx + 10, self.rect.y + 15)
        pygame.draw.circle(surface, RED, eye_l, 6)
        pygame.draw.circle(surface, RED, eye_r, 6)
        pygame.draw.circle(surface, BLACK, eye_l, 3)
        pygame.draw.circle(surface, BLACK, eye_r, 3)
        pygame.draw.circle(surface, WHITE, (eye_l[0] - 1, eye_l[1] - 1), 1)
        pygame.draw.circle(surface, WHITE, (eye_r[0] - 1, eye_r[1] - 1), 1)

        pygame.draw.polygon(surface, WHITE, [(self.rect.centerx - 7, self.rect.y + 28), (self.rect.centerx - 11, self.rect.y + 35), (self.rect.centerx - 4, self.rect.y + 33)])
        pygame.draw.polygon(surface, WHITE, [(self.rect.centerx + 7, self.rect.y + 28), (self.rect.centerx + 11, self.rect.y + 35), (self.rect.centerx + 4, self.rect.y + 33)])

        pygame.draw.line(surface, BLACK, (eye_l[0] - 5, eye_l[1] - 3), (eye_l[0] + 2, eye_l[1] + 2), 2)

        pygame.draw.line(surface, DARK_BROWN, (self.rect.x - 3, self.rect.centery - 5), (self.rect.x - 12, self.rect.centery), 5)
        pygame.draw.line(surface, DARK_BROWN, (self.rect.right + 3, self.rect.centery - 5), (self.rect.right + 12, self.rect.centery), 5)

        if self.hp < self.max_hp:
            bar_width = 40
            bar_height = 5
            bar_x = self.rect.x
            bar_y = self.rect.y - 10
            pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height))
            fill_width = int((self.hp / self.max_hp) * bar_width)
            pygame.draw.rect(surface, RED, (bar_x, bar_y, fill_width, bar_height))

    def update(self, player_rect):
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player_rect.y:
            self.rect.y -= self.speed

class Apple:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = APPLE_RED
        self.alive = True
        self.points = 250

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, 15)
        pygame.draw.line(surface, (100, 50, 0), (self.rect.centerx - 5, self.rect.top - 5), (self.rect.centerx, self.rect.top), 3)
        pygame.draw.circle(surface, (0, 100, 0), (self.rect.centerx - 8, self.rect.centery - 5), 3)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=15)

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Killer Time - Меню")
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont('Arial', 72, bold=True)
    font_normal = pygame.font.SysFont('Arial', 36)
    font_small = pygame.font.SysFont('Arial', 24)
    font_tiny = pygame.font.SysFont('Arial', 18)

    button_w = 220
    button_h = 70
    small_button_w = 190
    center_x = WIDTH // 2

    spacing = 30
    total_width = small_button_w * 4 + spacing * 3
    start_x = center_x - total_width // 2

    easy_button = Button(start_x, 250, small_button_w, button_h, "ЛЕГКИЙ", GREEN, font_size=28)
    normal_button = Button(start_x + small_button_w + spacing, 250, small_button_w, button_h, "СРЕДНИЙ", LIGHT_BLUE, font_size=28)
    hard_button = Button(start_x + 2 * (small_button_w + spacing), 250, small_button_w, button_h, "СЛОЖНЫЙ", ORANGE, font_size=28)
    hardcore_button = Button(start_x + 3 * (small_button_w + spacing), 250, small_button_w, button_h, "ХАРДКОР", PURPLE, font_size=28)

    selected_difficulty = "normal"

    start_button = Button(center_x - 150, 450, 300, 80, "НАЧАТЬ ИГРУ", LIGHT_BLUE, BLACK, font_size=36)
    quit_button = Button(center_x - 150, 570, 300, 80, "ВЫЙТИ", RED, WHITE, font_size=36)

    background = pygame.Surface((WIDTH, HEIGHT))
    for i in range(HEIGHT):
        color_value = 30 + i * 20 // HEIGHT
        pygame.draw.line(background, (color_value, color_value, 50 + i // 10), (0, i), (WIDTH, i))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        easy_button.check_hover(mouse_pos)
        normal_button.check_hover(mouse_pos)
        hard_button.check_hover(mouse_pos)
        hardcore_button.check_hover(mouse_pos)
        start_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        if easy_button.is_clicked(mouse_pos, mouse_click):
            selected_difficulty = "easy"
        elif normal_button.is_clicked(mouse_pos, mouse_click):
            selected_difficulty = "normal"
        elif hard_button.is_clicked(mouse_pos, mouse_click):
            selected_difficulty = "hard"
        elif hardcore_button.is_clicked(mouse_pos, mouse_click):
            selected_difficulty = "hardcore"
        elif start_button.is_clicked(mouse_pos, mouse_click):
            return selected_difficulty
        elif quit_button.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()

        screen.blit(background, (0, 0))

        title_shadow = font_title.render("Killer Time", True, (0, 0, 0))
        title_shadow_rect = title_shadow.get_rect(center=(WIDTH // 2 + 5, 85))
        screen.blit(title_shadow, title_shadow_rect)
        title = font_title.render("Killer Time", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title, title_rect)

        diff_text = font_normal.render("ВЫБЕРИТЕ СЛОЖНОСТЬ:", True, WHITE)
        diff_rect = diff_text.get_rect(center=(WIDTH // 2, 170))
        screen.blit(diff_text, diff_rect)

        easy_button.draw(screen, font_normal)
        normal_button.draw(screen, font_normal)
        hard_button.draw(screen, font_normal)
        hardcore_button.draw(screen, font_normal)

        desc_easy = font_tiny.render(DIFFICULTY_SETTINGS["easy"]["desc"], True, GRAY)
        desc_easy_rect = desc_easy.get_rect(center=(easy_button.rect.centerx, easy_button.rect.bottom + 15))
        screen.blit(desc_easy, desc_easy_rect)

        desc_normal = font_tiny.render(DIFFICULTY_SETTINGS["normal"]["desc"], True, GRAY)
        desc_normal_rect = desc_normal.get_rect(center=(normal_button.rect.centerx, normal_button.rect.bottom + 15))
        screen.blit(desc_normal, desc_normal_rect)

        desc_hard = font_tiny.render(DIFFICULTY_SETTINGS["hard"]["desc"], True, GRAY)
        desc_hard_rect = desc_hard.get_rect(center=(hard_button.rect.centerx, hard_button.rect.bottom + 15))
        screen.blit(desc_hard, desc_hard_rect)

        desc_hardcore = font_tiny.render(DIFFICULTY_SETTINGS["hardcore"]["desc"], True, GRAY)
        desc_hardcore_rect = desc_hardcore.get_rect(center=(hardcore_button.rect.centerx, hardcore_button.rect.bottom + 15))
        screen.blit(desc_hardcore, desc_hardcore_rect)

        selected_button = None
        if selected_difficulty == "easy":
            selected_button = easy_button
        elif selected_difficulty == "normal":
            selected_button = normal_button
        elif selected_difficulty == "hard":
            selected_button = hard_button
        elif selected_difficulty == "hardcore":
            selected_button = hardcore_button

        if selected_button:
            pygame.draw.rect(screen, GOLD, selected_button.rect.inflate(12, 12), 5, border_radius=20)

        start_button.draw(screen, font_normal)
        quit_button.draw(screen, font_normal)

        instruction = font_small.render("Управление: WASD - движение, ESC - меню", True, WHITE)
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        screen.blit(instruction, instruction_rect)

        pygame.display.flip()
        clock.tick(FPS)

def show_game_over(score):
    screen = pygame.display.get_surface()
    screen.fill((0, 0, 0))

    font = pygame.font.SysFont('Arial', 72, bold=True)
    font_small = pygame.font.SysFont('Arial', 36)

    game_over_text = font.render("ИГРА ОКОНЧЕНА", True, RED)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(game_over_text, game_over_rect)
    score_text = font_small.render(f"Ваш счет: {score}", True, YELLOW)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(score_text, score_rect)
    restart_text = font_small.render("Нажмите R для рестарта или ESC для выхода в меню", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"

def run_game(difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Killer Time Game")
    clock = pygame.time.Clock()

    settings = DIFFICULTY_SETTINGS[difficulty]

    player = Player(WIDTH // 2, HEIGHT // 2, GREEN, hp=100, speed=settings["player_speed"])
    enemies = []
    apples = []
    apples.append(Apple(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 30)))

    last_enemy_time = 0
    score = 0
    last_score_time = pygame.time.get_ticks()
    font = pygame.font.SysFont('Arial', 32, bold=True)

    difficulty_font = pygame.font.SysFont('Arial', 24)
    difficulty_names = {
        "easy": "ЛЕГКИЙ",
        "normal": "СРЕДНИЙ",
        "hard": "СЛОЖНЫЙ",
        "hardcore": "ХАРДКОР"
    }
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"

        if current_time - last_score_time >= 1000:
            score += 100
            last_score_time = current_time

        if current_time - last_enemy_time > settings["enemy_spawn_time"]:
            min_distance = 350
            safe = False
            attempts = 0
            while not safe and attempts < 30:
                enemy_x = random.randint(0, WIDTH - 40)
                enemy_y = random.randint(0, HEIGHT - 60)
                dx = (enemy_x + 20) - (player.rect.x + 20)
                dy = (enemy_y + 30) - (player.rect.y + 30)
                dist = math.hypot(dx, dy)
                if dist >= min_distance:
                    safe = True
                attempts += 1
            enemies.append(Enemy(enemy_x, enemy_y, settings["color"],
                                 hp=settings["enemy_hp"],
                                 speed=settings["enemy_speed"],
                                 damage=settings["enemy_damage"]))
            last_enemy_time = current_time

        keys = pygame.key.get_pressed()
        player.update(keys)

        for enemy in enemies[:]:
            enemy.update(player.rect)
            if enemy.rect.colliderect(player.rect):
                enemy.attack(player)
                if not player.alive:
                    player.hp = 0
                    result = show_game_over(score)
                    return result

        for enemy in enemies[:]:
            if not enemy.alive:
                enemies.remove(enemy)
                score += 10

        for apple in apples[:]:
            if apple.rect.colliderect(player.rect):
                score += apple.points
                apples.remove(apple)
                new_apple = Apple(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 30))
                apples.append(new_apple)

        screen.fill(WHITE)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for apple in apples:
            apple.draw(screen)

        score_shadow = font.render(f"Очки: {score}", True, GRAY)
        screen.blit(score_shadow, (12, 12))
        score_text = font.render(f"Очки: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        hp_value = player.hp if player.alive else 0
        hp_shadow = font.render(f"HP: {hp_value}", True, GRAY)
        screen.blit(hp_shadow, (12, 52))
        hp_text = font.render(f"HP: {hp_value}", True, BLACK)
        screen.blit(hp_text, (10, 50))

        diff_display = font.render(f"Сложность: {difficulty_names[difficulty]}", True, BLACK)
        diff_shadow = font.render(f"Сложность: {difficulty_names[difficulty]}", True, GRAY)
        screen.blit(diff_shadow, (12, 92))
        screen.blit(diff_display, (10, 90))

        instruction = font.render("WASD - двигаться, ESC - меню", True, BLACK)
        instruction_shadow = font.render("WASD - двигаться, ESC - меню", True, GRAY)
        screen.blit(instruction_shadow, (WIDTH // 2 - 148, HEIGHT - 38))
        screen.blit(instruction, (WIDTH // 2 - 150, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(FPS)
    return "menu"

def main():
    pygame.mixer.init()
    while True:
        difficulty = show_menu()
        while True:
            game_result = run_game(difficulty)
            if game_result == "restart":
                continue
            elif game_result == "menu":
                break
            else:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()