import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
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

PLAYER_SPEED = 25
ENEMY_SPEED = 5
ENEMY_SPAWN_TIME = 1000

DIFFICULTY_SETTINGS = {
    "easy": {
        "player_speed": 30,
        "enemy_speed": 3,
        "enemy_spawn_time": 2000,
        "enemy_hp": 30,
        "enemy_damage": 5,
        "color": GREEN,
        "desc": "Медленные враги, редко"
    },
    "normal": {
        "player_speed": 25,
        "enemy_speed": 5,
        "enemy_spawn_time": 1000,
        "enemy_hp": 50,
        "enemy_damage": 10,
        "color": LIGHT_BLUE,
        "desc": "Сбалансировано"
    },
    "hard": {
        "player_speed": 20,
        "enemy_speed": 7,
        "enemy_spawn_time": 700,
        "enemy_hp": 70,
        "enemy_damage": 15,
        "color": ORANGE,
        "desc": "Быстрые враги, часто"
    },
    "hardcore": {
        "player_speed": 15,
        "enemy_speed": 10,
        "enemy_spawn_time": 400,
        "enemy_hp": 100,
        "enemy_damage": 20,
        "color": PURPLE,
        "desc": "Очень быстро и опасно"
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
            pygame.draw.rect(surface, GOLD, self.rect.inflate(6, 6), border_radius=18)
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

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        if self.hp < self.max_hp:
            bar_width = 40
            bar_height = 5
            bar_x = self.rect.x
            bar_y = self.rect.y - 10
            pygame.draw.rect(surface, BLACK, (bar_x, bar_y, bar_width, bar_height))
            fill_width = int((self.hp / self.max_hp) * bar_width)
            pygame.draw.rect(surface, GREEN, (bar_x, bar_y, fill_width, bar_height))

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def attack(self, target):
        target.take_damage(self.damage)


class Player(Unit):
    def update(self, keys):
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


class Enemy(Unit):
    def update(self, player_rect):
        if self.rect.x < player_rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player_rect.x:
            self.rect.x -= self.speed
        if self.rect.y < player_rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player_rect.y:
            self.rect.y -= self.speed


def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Clash-like Game - Меню")
    clock = pygame.time.Clock()
    font_large = pygame.font.SysFont('Arial', 48, bold=True)
    font_normal = pygame.font.SysFont('Arial', 32)
    font_small = pygame.font.SysFont('Arial', 24)
    font_tiny = pygame.font.SysFont('Arial', 18)

    button_w, button_h = 260, 70
    small_button_w = 180
    center_x = WIDTH // 2 - button_w // 2

    easy_button = Button(center_x - 140, 150, small_button_w, button_h, "ЛЕГКИЙ", GREEN)
    normal_button = Button(center_x + 140, 150, small_button_w, button_h, "СРЕДНИЙ", LIGHT_BLUE)
    hard_button = Button(center_x - 140, 250, small_button_w, button_h, "СЛОЖНЫЙ", ORANGE)
    hardcore_button = Button(center_x + 140, 250, small_button_w, button_h, "ХАРДКОР", PURPLE)

    selected_difficulty = "normal"

    start_button = Button(center_x, 380, button_w, button_h, "НАЧАТЬ ИГРУ", LIGHT_BLUE)
    quit_button = Button(center_x, 480, button_w, button_h, "ВЫЙТИ", RED)

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

        screen.fill((30, 30, 50))

        title = font_large.render("CLASH-LIKE GAME", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title, title_rect)

        diff_text = font_normal.render("ВЫБЕРИТЕ СЛОЖНОСТЬ:", True, WHITE)
        diff_rect = diff_text.get_rect(center=(WIDTH // 2, 110))
        screen.blit(diff_text, diff_rect)

        easy_button.draw(screen, font_normal)
        normal_button.draw(screen, font_normal)
        hard_button.draw(screen, font_normal)
        hardcore_button.draw(screen, font_normal)

        desc_easy = font_tiny.render(DIFFICULTY_SETTINGS["easy"]["desc"], True, WHITE)
        desc_easy_rect = desc_easy.get_rect(center=(easy_button.rect.centerx, easy_button.rect.bottom + 15))
        screen.blit(desc_easy, desc_easy_rect)

        desc_normal = font_tiny.render(DIFFICULTY_SETTINGS["normal"]["desc"], True, WHITE)
        desc_normal_rect = desc_normal.get_rect(center=(normal_button.rect.centerx, normal_button.rect.bottom + 15))
        screen.blit(desc_normal, desc_normal_rect)

        desc_hard = font_tiny.render(DIFFICULTY_SETTINGS["hard"]["desc"], True, WHITE)
        desc_hard_rect = desc_hard.get_rect(center=(hard_button.rect.centerx, hard_button.rect.bottom + 15))
        screen.blit(desc_hard, desc_hard_rect)

        desc_hardcore = font_tiny.render(DIFFICULTY_SETTINGS["hardcore"]["desc"], True, WHITE)
        desc_hardcore_rect = desc_hardcore.get_rect(
            center=(hardcore_button.rect.centerx, hardcore_button.rect.bottom + 15))
        screen.blit(desc_hardcore, desc_hardcore_rect)

        if selected_difficulty == "easy":
            pygame.draw.rect(screen, GOLD, easy_button.rect.inflate(8, 8), 5, border_radius=18)
        elif selected_difficulty == "normal":
            pygame.draw.rect(screen, GOLD, normal_button.rect.inflate(8, 8), 5, border_radius=18)
        elif selected_difficulty == "hard":
            pygame.draw.rect(screen, GOLD, hard_button.rect.inflate(8, 8), 5, border_radius=18)
        elif selected_difficulty == "hardcore":
            pygame.draw.rect(screen, GOLD, hardcore_button.rect.inflate(8, 8), 5, border_radius=18)

        start_button.draw(screen, font_normal)
        quit_button.draw(screen, font_normal)

        instruction = font_small.render("Управление: WASD - движение, ESC - меню", True, GRAY)
        instruction_rect = instruction.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(instruction, instruction_rect)

        pygame.display.flip()
        clock.tick(FPS)


def show_game_over(score):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont('Arial', 72, bold=True)
    font_small = pygame.font.SysFont('Arial', 36)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
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
    pygame.display.set_caption("Clash-like Game")
    clock = pygame.time.Clock()

    settings = DIFFICULTY_SETTINGS[difficulty]

    player = Player(WIDTH // 2, HEIGHT // 2, BLUE, hp=200, speed=settings["player_speed"])
    enemies = []
    last_enemy_time = 0
    score = 0
    last_score_time = pygame.time.get_ticks()
    font = pygame.font.SysFont(None, 36)

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
            enemy_x = random.randint(0, WIDTH - 40)
            enemy_y = random.randint(0, HEIGHT - 60)
            enemies.append(Enemy(enemy_x, enemy_y, RED,
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
                    result = show_game_over(score)
                    return result

        for enemy in enemies[:]:
            if not enemy.alive:
                enemies.remove(enemy)
                score += 10

        screen.fill(WHITE)
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        score_text = font.render(f"Очки: {score}", True, BLACK)
        hp_text = font.render(f"HP: {player.hp}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(hp_text, (10, 50))

        diff_display = difficulty_font.render(f"Сложность: {difficulty_names[difficulty]}", True, BLACK)
        screen.blit(diff_display, (10, 90))

        instruction = font.render("WASD - двигаться, ESC - меню", True, BLACK)
        screen.blit(instruction, (WIDTH // 2 - 150, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(FPS)
    return "menu"


def main():
    pygame.mixer.init()
    while True:
        difficulty = show_menu()
        game_result = run_game(difficulty)
        if game_result == "restart":
            continue
        elif game_result == "menu":
            continue
        else:
            break


if __name__ == "__main__":
    main()