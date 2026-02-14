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
PURPLE = (128, 0, 128)

PLAYER_SPEED = 25
ENEMY_SPEED = 5
ENEMY_SPAWN_TIME = 1000

class Button:
    def __init__(self, x, y, w, h, text, color=LIGHT_BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hovered = False
    def draw(self, surface, font):
        color = self.color
        if self.hovered:
            color = (min(self.color[0]+30,255), min(self.color[1]+30,255), min(self.color[2]+30,255))
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=15)
        text_surf = font.render(self.text, True, BLACK)
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
    button_w, button_h = 300, 60
    center_x = WIDTH // 2 - button_w // 2
    start_button = Button(center_x, 250, button_w, button_h, "НАЧАТЬ ИГРУ")
    quit_button = Button(center_x, 350, button_w, button_h, "ВЫЙТИ", RED)
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
        start_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        if start_button.is_clicked(mouse_pos, mouse_click):
            return "start"
        elif quit_button.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()
        screen.fill((30, 30, 50))
        title = font_large.render("CLASH-LIKE GAME", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        screen.blit(title, title_rect)
        subtitle = font_small.render("Нажмите 'НАЧАТЬ ИГРУ' чтобы начать", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 180))
        screen.blit(subtitle, subtitle_rect)
        start_button.draw(screen, font_normal)
        quit_button.draw(screen, font_normal)
        instruction = font_small.render("Управление: WASD - движение, ESC - меню", True, GRAY)
        instruction_rect = instruction.get_rect(center=(WIDTH//2, HEIGHT - 50))
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
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
    screen.blit(game_over_text, game_over_rect)
    score_text = font_small.render(f"Ваш счет: {score}", True, YELLOW)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(score_text, score_rect)
    restart_text = font_small.render("Нажмите R для рестарта или ESC для выхода в меню", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
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

def run_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Clash-like Game")
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT // 2, BLUE, hp=200, speed=PLAYER_SPEED)
    enemies = []
    last_enemy_time = 0
    score = 0
    last_score_time = pygame.time.get_ticks()
    font = pygame.font.SysFont(None, 36)
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
        if current_time - last_enemy_time > ENEMY_SPAWN_TIME:
            enemy_x = random.randint(0, WIDTH - 40)
            enemy_y = random.randint(0, HEIGHT - 60)
            enemies.append(Enemy(enemy_x, enemy_y, RED, hp=50, speed=ENEMY_SPEED, damage=10))
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
        instruction = font.render("WASD - двигаться, ESC - меню", True, BLACK)
        screen.blit(instruction, (WIDTH // 2 - 300, HEIGHT - 40))
        pygame.display.flip()
        clock.tick(FPS)
    return "menu"

def main():
    pygame.mixer.init()
    while True:
        menu_result = show_menu()
        if menu_result == "start":
            game_result = run_game()
            if game_result == "restart":
                continue
            elif game_result == "menu":
                continue
        else:
            break

if __name__ == "__main__":
    main()