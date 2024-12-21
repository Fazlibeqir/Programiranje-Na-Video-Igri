import pygame
import random

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Load resources
background_music = 'Resources/background_music.wav'
clash_sound_file = 'Resources/clash_sound.wav'
spaceship_image = 'Resources/spaceship.png'
asteroid_image = 'Resources/asteroid.png'
energy_crystal_image = 'Resources/energy_crystal.png'

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Scavenger")

# Load images with scaling
spaceship_img = pygame.transform.scale(pygame.image.load(spaceship_image).convert_alpha(), (50, 50))
asteroid_img = pygame.transform.scale(pygame.image.load(asteroid_image).convert_alpha(), (50, 50))
energy_crystal_img = pygame.transform.scale(pygame.image.load(energy_crystal_image).convert_alpha(), (30, 30))

# Load sounds
pygame.mixer.music.load(background_music)
clash_sound = pygame.mixer.Sound(clash_sound_file)

# Play background music
pygame.mixer.music.play(-1)

# Font for displaying score
font = pygame.font.Font(None, 36)


# Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = spaceship_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 4) * speed_multiplier

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)


# Energy Crystal class
class EnergyCrystal(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1):
        super().__init__()
        self.image = energy_crystal_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3) * speed_multiplier

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)


# Main function
def main():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    energy_crystals = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Create spaceship
    spaceship = Spaceship()
    all_sprites.add(spaceship)

    # Create asteroids and crystals
    for _ in range(5):
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroids.add(asteroid)

    for _ in range(3):
        crystal = EnergyCrystal()
        all_sprites.add(crystal)
        energy_crystals.add(crystal)

    # Game variables
    score = 0
    time_score = 0
    clock = pygame.time.Clock()
    running = True
    speed_multiplier = 1  # Starting speed multiplier

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Shoot a bullet
                bullet = Bullet(spaceship.rect.centerx, spaceship.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

        # Update
        all_sprites.update()

        time_score += 0.1
        total_score = score + int(time_score)

        # Check for collisions
        if pygame.sprite.spritecollideany(spaceship, asteroids):
            clash_sound.play()
            display_message("Game Over!", RED)
            running = False

        energy_crystal_hit = pygame.sprite.spritecollide(spaceship, energy_crystals, dokill=True)
        if energy_crystal_hit:
            score += 10
            new_crystal = EnergyCrystal(speed_multiplier)
            all_sprites.add(new_crystal)
            energy_crystals.add(new_crystal)

        for bullet in bullets:
            asteroid_hit = pygame.sprite.spritecollide(bullet, asteroids, dokill=False)
            if asteroid_hit:
                bullet.kill()
                for asteroid in asteroid_hit:
                    asteroid.rect.x = random.randint(0, SCREEN_WIDTH - asteroid.rect.width)
                    asteroid.rect.y = random.randint(-100, -40)
                    asteroid.speed = random.randint(1, 4) * speed_multiplier

        # Gradual difficulty adjustment
        if score > 0 and score % 5 == 0:
            if speed_multiplier < 2:  # Cap the maximum speed multiplier
                speed_multiplier += 0.05  # Small increment for gradual progression
            for asteroid in asteroids:
                asteroid.speed = random.randint(1, 4) * speed_multiplier

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


def display_message(text, color):
    screen.fill(BLACK)  # Clear the screen
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)


if __name__ == "__main__":
    main()
