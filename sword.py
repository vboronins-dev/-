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

DIFFICULTY_SETTINGS = {
    "easy": {
        "player_speed": 10,
        "enemy_speed": 1.5,
        "enemy_spawn_time": 1500,
        "enemy_hp": 30,
        "enemy_damage": 2,
        "color": BROWN,
        "desc": "Медленные враги, очень просто"
    },
    "normal": {
        "player_speed": 10,
        "enemy_speed": 3,
        "enemy_spawn_time": 1500,
        "enemy_hp": 50,
        "enemy_damage": 2,
        "color": BROWN,
        "desc": "Сбалансировано"
    },
    "hard": {
        "player_speed": 10,
        "enemy_speed": 4.5,
        "enemy_spawn_time": 1500,
        "enemy_hp": 70,
        "enemy_damage": 2,
        "color": DARK_BROWN,
        "desc": "Быстрые враги, сложно"
    },
    "hardcore": {
        "player_speed": 10,
        "enemy_speed": 5.5,
        "enemy_spawn_time": 1500,
        "enemy_hp": 100,
        "enemy_damage": 2,
        "color": DARKER_BROWN,
        "desc": "Очень быстро и сложно"
    }
}

class Button:
    def __init__(self, x, y, w, h, text, color=LIGHT_BLUE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface, font):
        color = self.color
        if self.hovered:
            color = (min(self.color[0] + 40, 255), min(self.color[1] + 40, 255), min(self.color[2] + 40, 255))
            pygame.draw.rect(surface, GOLD, self.rect.inflate(8, 8), border_radius=18, width=4)
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

class AttackBall:
    def __init__(self, center_x, center_y, radius, damage, duration):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.damage = damage
        self.duration = duration
        self.active = True
        self.angle = 0
        self.ball_radius = 15

    def update(self, player_rect):
        self.center_x = player_rect.centerx
        self.center_y = player_rect.centery
        self.angle += 0.1
        self.duration -= 1
        if self.duration <= 0:
            self.active = False

    def draw(self, surface):
        if not self.active:
            return
        for i in range(8):
            angle_offset = self.angle + i * math.pi * 2 / 8
            ball_x = self.center_x + math.cos(angle_offset) * self.radius
            ball_y = self.center_y + math.sin(angle_offset) * self.radius
            pygame.draw.circle(surface, (255, 200, 0), (int(ball_x), int(ball_y)), self.ball_radius)
            pygame.draw.circle(surface, (255, 100, 0), (int(ball_x), int(ball_y)), self.ball_radius - 3)
            pygame.draw.circle(surface, (255, 255, 255), (int(ball_x), int(ball_y)), self.ball_radius - 6)

    def check_collision(self, enemy_rect):
        if not self.active:
            return False
        for i in range(8):
            angle_offset = self.angle + i * math.pi * 2 / 8
            ball_x = self.center_x + math.cos(angle_offset) * self.radius
            ball_y = self.center_y + math.sin(angle_offset) * self.radius
            ball_rect = pygame.Rect(ball_x - self.ball_radius, ball_y - self.ball_radius,
                                    self.ball_radius * 2, self.ball_radius * 2)
            if ball_rect.colliderect(enemy_rect):
                return True
        return False

class Player(Unit):
    def __init__(self, x, y, color, hp=100, speed=5, damage=10):
        super().__init__(x, y, color, hp, speed, damage)
        self.rect = pygame.Rect(x, y, 30, 45)
        self.animation_offset = 0
        self.animation_direction = 1
        self.attack_animation = 0

    def draw(self, surface):
        self.animation_offset += 0.1 * self.animation_direction
        if self.animation_offset > 2 or self.animation_offset < -2:
            self.animation_direction *= -1

        if self.attack_animation > 0:
            self.attack_animation -= 1

        body_rect = self.rect.inflate(-5, -5)
        pygame.draw.rect(surface, DARK_GREEN, self.rect, border_radius=6)
        pygame.draw.rect(surface, GREEN, body_rect, border_radius=4)

        belt_y = self.rect.y + 26
        pygame.draw.rect(surface, RED, (self.rect.x + 4, belt_y, 22, 5), border_radius=2)
        pygame.draw.rect(surface, (200, 0, 0), (self.rect.x + 6, belt_y + 1, 18, 3), border_radius=1)

        for i in range(2):
            line_y = self.rect.y + 14 + i * 9
            pygame.draw.line(surface, DARK_GREEN, (self.rect.x + 6, line_y), (self.rect.x + 24, line_y), 2)

        head_center = (self.rect.centerx, self.rect.y - 6 + self.animation_offset)
        pygame.draw.circle(surface, SKIN, head_center, 9)
        pygame.draw.circle(surface, (230, 180, 130), head_center, 7)

        pygame.draw.rect(surface, BLACK, (head_center[0] - 9, head_center[1] - 7, 18, 6), border_radius=3)
        pygame.draw.line(surface, RED, (head_center[0] - 6, head_center[1] - 4), (head_center[0] + 6, head_center[1] - 4), 2)

        pygame.draw.circle(surface, WHITE, (head_center[0] - 3, head_center[1]), 2)
        pygame.draw.circle(surface, WHITE, (head_center[0] + 3, head_center[1]), 2)
        pygame.draw.circle(surface, BLACK, (head_center[0] - 3, head_center[1]), 1)
        pygame.draw.circle(surface, BLACK, (head_center[0] + 3, head_center[1]), 1)

        mask = pygame.Rect(head_center[0] - 5, head_center[1] + 3, 10, 4)
        pygame.draw.rect(surface, DARK_GREEN, mask, border_radius=1)

        sword_x = self.rect.right - 5
        sword_y = self.rect.y + 18
        if self.attack_animation > 0:
            pygame.draw.line(surface, GRAY, (sword_x, sword_y), (sword_x + 25, sword_y - 12), 3)
            pygame.draw.line(surface, (139, 69, 19), (sword_x - 3, sword_y), (sword_x, sword_y), 2)
        else:
            pygame.draw.line(surface, GRAY, (sword_x, sword_y), (sword_x + 15, sword_y - 5), 2)
            pygame.draw.line(surface, (139, 69, 19), (sword_x - 3, sword_y), (sword_x, sword_y), 2)

        pygame.draw.rect(surface, GREEN, (self.rect.x - 3, self.rect.y + 11, 5, 15), border_radius=2)
        pygame.draw.rect(surface, GREEN, (self.rect.right - 2, self.rect.y + 11, 5, 15), border_radius=2)

        pygame.draw.rect(surface, DARK_GREEN, (self.rect.x + 5, self.rect.bottom - 12, 6, 13), border_radius=2)
        pygame.draw.rect(surface, DARK_GREEN, (self.rect.x + 19, self.rect.bottom - 12, 6, 13), border_radius=2)

        if self.hp < self.max_hp:
            bar_width = 30
            bar_height = 4
            bar_x = self.rect.x
            bar_y = self.rect.y - 8
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
        self.rect = pygame.Rect(x, y, 40, 60)
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
            pygame.draw.polygon(surface, DARKER_BROWN,
                                [(spike_x, spike_y), (spike_x + 8, spike_y - 6), (spike_x + 4, spike_y + 4)])

        for _ in range(6):
            cx = self.rect.x + random.randint(8, 32)
            cy = self.rect.y + random.randint(8, 52)
            pygame.draw.line(surface, DARKER_BROWN, (cx, cy),
                             (cx + random.randint(-4, 4), cy + random.randint(-4, 4)), 2)

        eye_l = (self.rect.centerx - 10, self.rect.y + 15)
        eye_r = (self.rect.centerx + 10, self.rect.y + 15)
        pygame.draw.circle(surface, RED, eye_l, 6)
        pygame.draw.circle(surface, RED, eye_r, 6)
        pygame.draw.circle(surface, BLACK, eye_l, 3)
        pygame.draw.circle(surface, BLACK, eye_r, 3)
        pygame.draw.circle(surface, WHITE, (eye_l[0] - 1, eye_l[1] - 1), 1)
        pygame.draw.circle(surface, WHITE, (eye_r[0] - 1, eye_r[1] - 1), 1)

        pygame.draw.polygon(surface, WHITE,
                            [(self.rect.centerx - 7, self.rect.y + 28),
                             (self.rect.centerx - 11, self.rect.y + 35),
                             (self.rect.centerx - 4, self.rect.y + 33)])
        pygame.draw.polygon(surface, WHITE,
                            [(self.rect.centerx + 7, self.rect.y + 28),
                             (self.rect.centerx + 11, self.rect.y + 35),
                             (self.rect.centerx + 4, self.rect.y + 33)])

        pygame.draw.line(surface, BLACK, (eye_l[0] - 5, eye_l[1] - 3), (eye_l[0] + 2, eye_l[1] + 2), 2)

        pygame.draw.line(surface, DARK_BROWN, (self.rect.x - 3, self.rect.centery - 5),
                         (self.rect.x - 12, self.rect.centery), 5)
        pygame.draw.line(surface, DARK_BROWN, (self.rect.right + 3, self.rect.centery - 5),
                         (self.rect.right + 12, self.rect.centery), 5)

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
        pygame.draw.line(surface, (100, 50, 0), (self.rect.centerx - 5, self.rect.top - 5),
                         (self.rect.centerx, self.rect.top), 3)
        pygame.draw.circle(surface, (0, 100, 0), (self.rect.centerx - 8, self.rect.centery - 5), 3)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=15)

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Green Ninja - Меню")
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

    easy_btn = Button(start_x, 250, small_button_w, button_h, "ЛЕГКИЙ", GREEN)
    normal_btn = Button(start_x + small_button_w + spacing, 250, small_button_w, button_h, "СРЕДНИЙ", LIGHT_BLUE)
    hard_btn = Button(start_x + 2 * (small_button_w + spacing), 250, small_button_w, button_h, "СЛОЖНЫЙ", ORANGE)
    hardcore_btn = Button(start_x + 3 * (small_button_w + spacing), 250, small_button_w, button_h, "ХАРДКОР", PURPLE)

    selected = "normal"

    start_btn = Button(center_x - 150, 450, 300, 80, "НАЧАТЬ ИГРУ", LIGHT_BLUE)
    quit_btn = Button(center_x - 150, 570, 300, 80, "ВЫЙТИ", RED, WHITE)

    background = pygame.Surface((WIDTH, HEIGHT))
    for i in range(HEIGHT):
        color_val = 30 + i * 20 // HEIGHT
        pygame.draw.line(background, (color_val, color_val, 50 + i // 10), (0, i), (WIDTH, i))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        easy_btn.check_hover(mouse_pos)
        normal_btn.check_hover(mouse_pos)
        hard_btn.check_hover(mouse_pos)
        hardcore_btn.check_hover(mouse_pos)
        start_btn.check_hover(mouse_pos)
        quit_btn.check_hover(mouse_pos)

        if easy_btn.is_clicked(mouse_pos, mouse_click):
            selected = "easy"
        elif normal_btn.is_clicked(mouse_pos, mouse_click):
            selected = "normal"
        elif hard_btn.is_clicked(mouse_pos, mouse_click):
            selected = "hard"
        elif hardcore_btn.is_clicked(mouse_pos, mouse_click):
            selected = "hardcore"
        elif start_btn.is_clicked(mouse_pos, mouse_click):
            return selected
        elif quit_btn.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()

        screen.blit(background, (0, 0))

        title_shadow = font_title.render("Green Ninja", True, (0, 0, 0))
        title_shadow_rect = title_shadow.get_rect(center=(WIDTH // 2 + 5, 85))
        screen.blit(title_shadow, title_shadow_rect)
        title = font_title.render("Green Ninja", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title, title_rect)

        diff_text = font_normal.render("ВЫБЕРИТЕ СЛОЖНОСТЬ:", True, WHITE)
        diff_rect = diff_text.get_rect(center=(WIDTH // 2, 170))
        screen.blit(diff_text, diff_rect)

        easy_btn.draw(screen, font_normal)
        normal_btn.draw(screen, font_normal)
        hard_btn.draw(screen, font_normal)
        hardcore_btn.draw(screen, font_normal)

        desc_y = hardcore_btn.rect.bottom + 15
        for btn, key in [(easy_btn, "easy"), (normal_btn, "normal"),
                         (hard_btn, "hard"), (hardcore_btn, "hardcore")]:
            desc = font_tiny.render(DIFFICULTY_SETTINGS[key]["desc"], True, GRAY)
            rect = desc.get_rect(center=(btn.rect.centerx, desc_y))
            screen.blit(desc, rect)

        selected_btn = None
        if selected == "easy":
            selected_btn = easy_btn
        elif selected == "normal":
            selected_btn = normal_btn
        elif selected == "hard":
            selected_btn = hard_btn
        elif selected == "hardcore":
            selected_btn = hardcore_btn
        if selected_btn:
            pygame.draw.rect(screen, GOLD, selected_btn.rect.inflate(12, 12), 5, border_radius=20)

        start_btn.draw(screen, font_normal)
        quit_btn.draw(screen, font_normal)

        instruction = font_small.render("Управление: WASD - движение, ESC - меню, SPACE - атака", True, WHITE)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_ESCAPE:
                    return "menu"

def run_game(difficulty):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Green Ninja Game")
    clock = pygame.time.Clock()

    settings = DIFFICULTY_SETTINGS[difficulty]

    player = Player(WIDTH // 2, HEIGHT // 2, GREEN, hp=100, speed=settings["player_speed"])
    enemies = []
    apples = [Apple(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 30))]

    last_enemy_time = 0
    score = 0
    last_score_time = pygame.time.get_ticks()
    font = pygame.font.SysFont('Arial', 16, bold=True)

    ATTACK_COOLDOWN_MAX = 1800
    ATTACK_DAMAGE = 30
    ATTACK_RADIUS = 65
    ATTACK_DURATION = 45
    SPAWN_MIN_DISTANCE = 350

    attack_ball = None
    attack_cooldown = 0

    difficulty_names = {"easy": "ЛЕГКИЙ", "normal": "СРЕДНИЙ", "hard": "СЛОЖНЫЙ", "hardcore": "ХАРДКОР"}

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        if attack_cooldown > 0:
            attack_cooldown -= 1

        keys = pygame.key.get_pressed()
        player.update(keys)

        if keys[pygame.K_SPACE] and attack_cooldown == 0 and (attack_ball is None or not attack_ball.active):
            attack_cooldown = ATTACK_COOLDOWN_MAX
            player.attack_animation = 8
            attack_ball = AttackBall(player.rect.centerx, player.rect.centery,
                                     ATTACK_RADIUS, ATTACK_DAMAGE, ATTACK_DURATION)

        if attack_ball is not None:
            attack_ball.update(player.rect)
            if not attack_ball.active:
                attack_ball = None

        if attack_ball is not None:
            for enemy in enemies[:]:
                if attack_ball.check_collision(enemy.rect):
                    enemy.take_damage(ATTACK_DAMAGE)
                    if not enemy.alive:
                        enemies.remove(enemy)
                        score += 250

        if current_time - last_score_time >= 1000:
            score += 100
            last_score_time = current_time

        if current_time - last_enemy_time > settings["enemy_spawn_time"]:
            safe = False
            attempts = 0
            while not safe and attempts < 30:
                enemy_x = random.randint(0, WIDTH - 40)
                enemy_y = random.randint(0, HEIGHT - 60)
                dx = (enemy_x + 20) - (player.rect.x + 15)
                dy = (enemy_y + 30) - (player.rect.y + 22)
                if math.hypot(dx, dy) >= SPAWN_MIN_DISTANCE:
                    safe = True
                attempts += 1
            enemies.append(Enemy(enemy_x, enemy_y, settings["color"],
                                 hp=settings["enemy_hp"],
                                 speed=settings["enemy_speed"],
                                 damage=settings["enemy_damage"]))
            last_enemy_time = current_time

        for enemy in enemies[:]:
            enemy.update(player.rect)
            if enemy.rect.colliderect(player.rect):
                enemy.attack(player)
                if not player.alive:
                    player.hp = 0
                    result = show_game_over(score)
                    return result

        for apple in apples[:]:
            if apple.rect.colliderect(player.rect):
                score += apple.points
                apples.remove(apple)
                apples.append(Apple(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 30)))

        screen.fill(WHITE)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for apple in apples:
            apple.draw(screen)
        if attack_ball is not None:
            attack_ball.draw(screen)

        score_shadow = font.render(f"Очки: {score}", True, GRAY)
        screen.blit(score_shadow, (3, 3))
        score_text = font.render(f"Очки: {score}", True, BLACK)
        screen.blit(score_text, (2, 2))

        hp_val = player.hp if player.alive else 0
        hp_shadow = font.render(f"HP: {hp_val}", True, GRAY)
        screen.blit(hp_shadow, (3, 23))
        hp_text = font.render(f"HP: {hp_val}", True, BLACK)
        screen.blit(hp_text, (2, 22))

        diff_display = font.render(f"Сложность: {difficulty_names[difficulty]}", True, BLACK)
        diff_shadow = font.render(f"Сложность: {difficulty_names[difficulty]}", True, GRAY)
        screen.blit(diff_shadow, (3, 43))
        screen.blit(diff_display, (2, 42))

        if attack_cooldown > 0:
            cd_text = font.render(f"Атака через: {attack_cooldown // 60 + 1}", True, RED)
            cd_rect = cd_text.get_rect(topright=(WIDTH - 5, 5))
            screen.blit(cd_text, cd_rect)

        instruction = font.render("WASD - двигаться, SPACE - атака, ESC - меню", True, BLACK)
        instruction_shadow = font.render("WASD - двигаться, SPACE - атака, ESC - меню", True, GRAY)
        inst_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 20))
        shadow_rect = instruction_shadow.get_rect(center=(WIDTH // 2 + 1, HEIGHT - 19))
        screen.blit(instruction_shadow, shadow_rect)
        screen.blit(instruction, inst_rect)

        pygame.display.flip()
        clock.tick(FPS)

    return "menu"

def main():
    pygame.mixer.init()
    while True:
        diff = show_menu()
        while True:
            result = run_game(diff)
            if result == "restart":
                continue
            elif result == "menu":
                break
            else:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()