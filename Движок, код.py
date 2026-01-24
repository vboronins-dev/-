import pygame
import random
import sys
pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
BLACK = (0, 0, 0)
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")


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


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player(WIDTH//2, HEIGHT//2, BLUE, hp = 200, speed = 5)
    enemies = []
    last_enemy_time = 0
    score = 0
    font = pygame.font.SysFont(None, 36)
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_enemy = Enemy(mouse_x, mouse_y, RED, hp = 50, speed = 2, damage = 10)
                enemies.append(new_enemy)
                print(f"Ваш враг создан в ({mouse_x}, {mouse_y})")

        if current_time - last_enemy_time > 2000:
            enemy_x = random.randint(0, WIDTH - 40)
            enemy_y = random.randint(0, HEIGHT - 60)
            enemies.append(Enemy(enemy_x, enemy_y, RED, hp = 50, speed = 2, damage = 10))
            last_enemy_time = current_time
            print(f"Авто-создан враг. Всего врагов: {len(enemies)}")

        keys = pygame.key.get_pressed()
        player.update(keys)

        for enemy in enemies[:]:
            enemy.update(player.rect)
            if enemy.rect.colliderect(player.rect):
                enemy.attack(player)
                if not player.alive:
                    running = False

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

        instruction = font.render("WASD - двигаться, Клик мыши - создать врага", True, BLACK)
        screen.blit(instruction, (WIDTH // 2 - 250, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()
    sys.exit()

if __name__ == "main":
    main()





