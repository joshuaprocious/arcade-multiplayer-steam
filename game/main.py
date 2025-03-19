import pygame
import math

# Pygame setup
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()

# World and Camera Settings
WORLD_SIZE = 3000
camera_x, camera_y = 0, 0
zoom = 1.0
follow_speed = 0.05
zoom_target = 1.0

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (20, 20, 20)

machine_gun = False

# Minimap Setup
MINIMAP_SIZE = 200
minimap_rect = pygame.Rect(WIDTH - MINIMAP_SIZE - 10, 10, MINIMAP_SIZE, MINIMAP_SIZE)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self.image.fill(BLUE)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(WORLD_SIZE // 2, WORLD_SIZE // 2))

    def update(self, keys):
        vel = 5
        if keys[pygame.K_w]: self.rect.y -= vel
        if keys[pygame.K_s]: self.rect.y += vel
        if keys[pygame.K_a]: self.rect.x -= vel
        if keys[pygame.K_d]: self.rect.x += vel

        # Keep within world bounds
        self.rect.x = max(0, min(self.rect.x, WORLD_SIZE - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, WORLD_SIZE - self.rect.height))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, angle):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.image.fill(RED)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 18
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Remove if out of bounds
        if not (0 <= self.rect.x <= WORLD_SIZE and 0 <= self.rect.y <= WORLD_SIZE):
            self.kill()

# Sprite Groups
player = Player()
player_group = pygame.sprite.GroupSingle(player)
bullets = pygame.sprite.Group()

def shoot_bullet():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    world_mouse_x = (mouse_x / zoom) + camera_x
    world_mouse_y = (mouse_y / zoom) + camera_y
    angle = math.atan2(world_mouse_y - player.rect.centery, world_mouse_x - player.rect.centerx)
    
    bullet = Bullet(player.rect.center, angle)
    bullets.add(bullet)

def update_camera():
    global camera_x, camera_y, zoom
    target_x = player.rect.centerx - (WIDTH / 2) / zoom
    target_y = player.rect.centery - (HEIGHT / 2) / zoom
    camera_x += (target_x - camera_x) * follow_speed
    camera_y += (target_y - camera_y) * follow_speed
    zoom += (zoom_target - zoom) * 0.1

def draw_grid():
    spacing = 500
    for x in range(0, WORLD_SIZE + 1, spacing):
        screen_x = (x - camera_x) * zoom
        if 0 <= screen_x <= WIDTH:
            pygame.draw.line(screen, GRAY, (screen_x, (0 - camera_y) * zoom), (screen_x, (WORLD_SIZE - camera_y) * zoom))

    for y in range(0, WORLD_SIZE + 1, spacing):
        screen_y = (y - camera_y) * zoom
        if 0 <= screen_y <= HEIGHT:
            pygame.draw.line(screen, GRAY, ((0 - camera_x) * zoom, screen_y), ((WORLD_SIZE - camera_x) * zoom, screen_y))

def draw_world():
    screen.fill(BLACK)
    draw_grid()
    
    # Draw world boundary
    pygame.draw.rect(screen, WHITE, pygame.Rect(-camera_x * zoom, -camera_y * zoom, WORLD_SIZE * zoom, WORLD_SIZE * zoom), 3)

    # Draw player (ensure it doesn't scale with zoom)
    for entity in player_group:
        scaled_player = pygame.transform.scale(entity.image, (int(entity.rect.width * zoom), int(entity.rect.height * zoom)))
        screen.blit(scaled_player, (
            (entity.rect.x - camera_x) * zoom, 
            (entity.rect.y - camera_y) * zoom
        ))

    # Draw bullets (they should still scale with zoom)
    for bullet in bullets:
        screen.blit(pygame.transform.scale(bullet.image, (10 * zoom, 10 * zoom)), ( 
            (bullet.rect.x - camera_x) * zoom, 
            (bullet.rect.y - camera_y) * zoom
        ))

    # Draw FPS counter
    fps = int(clock.get_fps())
    font = pygame.font.Font(None, 24)
    fps_text = font.render(f"FPS: {fps}", True, WHITE)
    screen.blit(fps_text, (10, 10))


def main():
    global zoom_target, machine_gun
    running = True

    TARGET_FPS = 120  # Render at 120 FPS
    TARGET_TICK_RATE = 60  # Game logic updates at 60 FPS
    TIME_PER_UPDATE = 1.0 / TARGET_TICK_RATE  # Fixed timestep for logic updates

    last_update_time = pygame.time.get_ticks() / 1000.0  # Get current time in seconds
    accumulator = 0.0

    while running:
        current_time = pygame.time.get_ticks() / 1000.0  # Convert milliseconds to seconds
        elapsed_time = current_time - last_update_time
        last_update_time = current_time
        accumulator += elapsed_time

        # Process events
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    machine_gun = True
                elif event.button == 4:  # Scroll Up
                    zoom_target = min(2.0, zoom_target + 0.1)
                elif event.button == 5:  # Scroll Down
                    zoom_target = max(0.5, zoom_target - 0.1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    machine_gun = False

        # **Update logic at a fixed rate (60 FPS)**
        while accumulator >= TIME_PER_UPDATE:
            player_group.update(keys)
            bullets.update()
            update_camera()

            if machine_gun and pygame.time.get_ticks() % 100 < 20:
                shoot_bullet()

            accumulator -= TIME_PER_UPDATE  # Reduce accumulated time

        # **Render as fast as possible (120 FPS)**
        draw_world()
        pygame.display.flip()

        clock.tick(TARGET_FPS)  # Cap rendering frame rate to 120 FPS

    pygame.quit()


if __name__ == "__main__":
    main()