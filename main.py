# Space Shooter Game
# Original by Tom Strzyz, Modified to add sound effects and CV2 video support

import pygame
import time
import random
import json
import os
import cv2
import numpy as np
from pygame import mixer
# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
    MOUSEBUTTONDOWN,
)

pygame.init()
mixer.init()  # Initialize sound mixer

# Load sound effects
try:
    shoot_sound = mixer.Sound("sounds/shoot.wav")
    explosion_sound = mixer.Sound("sounds/explosion.wav")
    elevator_music = mixer.Sound("sounds/elevator.mp3")
    theme_music = mixer.Sound("sounds/theme.mp3")

    # Adjust volumes
    shoot_sound.set_volume(0.5)
    explosion_sound.set_volume(0.7)
    elevator_music.set_volume(0.3)
    theme_music.set_volume(0.4)

    # Start playing theme music on loop
    theme_music.play(-1)
except Exception as e:
    print(f"Warning: Some sound files couldn't be loaded: {e}")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.width = 30
        self.height = 30
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.score = 0

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def resize(self, increase=True):
        if increase:
            self.width += 10
            self.height += 10
        else:
            self.width = max(10, self.width - 10)
            self.height = max(10, self.height - 10)

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=self.rect.center)

    def die(self):
        try:
            explosion_sound.play()
        except:
            pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width=10, height=5):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center=(x, y))
        try:
            shoot_sound.play()
        except:
            pass

    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, level=1):
        super(Enemy, self).__init__()
        base_width = random.randint(20, 50)
        base_height = random.randint(10, 30)
        width = base_width * (1.5 if level == 2 else 1)
        height = base_height * (1.5 if level == 2 else 1)

        self.surf = pygame.Surface((width, height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(
            8, 15) if level == 2 else random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def play_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame from BGR to RGB and rotate if needed
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)

            # Scale the frame to fit the screen if needed
            frame = pygame.transform.scale(
                frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

            screen.blit(frame, (0, 0))
            pygame.display.flip()

            # Handle events during video playback
            for event in pygame.event.get():
                if event.type == KEYDOWN or event.type == QUIT:
                    cap.release()
                    return

            clock.tick(30)

        cap.release()
    except Exception as e:
        print(f"Warning: Could not play video: {e}")


def pause_game():
    paused = True
    try:
        theme_music.stop()  # Stop theme music during pause
        elevator_music.play(-1)
    except:
        pass

    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    try:
                        elevator_music.stop()
                        theme_music.play(-1)  # Resume theme music
                    except:
                        pass
                    return True

        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text, text_rect)
        pygame.display.flip()


BLACK = (0, 0, 0)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()


def save_game(player, current_level):
    game_state = {
        "player_pos": (player.rect.x, player.rect.y),
        "player_size": (player.width, player.height),
        "score": player.score,
        "level": current_level
    }
    with open("savegame.json", "w") as f:
        json.dump(game_state, f)


def load_game():
    try:
        with open("savegame.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def show_main_menu():
    start_button = Button(SCREEN_WIDTH//2 - 100, 150, 200,
                          50, "Start Game", (0, 128, 0))
    load_button = Button(SCREEN_WIDTH//2 - 100, 250, 200,
                         50, "Load Game", (0, 0, 128))
    level_button = Button(SCREEN_WIDTH//2 - 100, 350, 200,
                          50, "Select Level", (128, 0, 0))

    running = True
    while running:
        screen.fill(BLACK)

        font = pygame.font.Font(None, 74)
        title = font.render("Space Shooter", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title, title_rect)

        start_button.draw(screen)
        load_button.draw(screen)
        level_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.is_clicked(mouse_pos):
                    return "start"
                elif load_button.is_clicked(mouse_pos):
                    return "load"
                elif level_button.is_clicked(mouse_pos):
                    return "level"


def show_level_select():
    level1_button = Button(SCREEN_WIDTH//2 - 100, 200,
                           200, 50, "Level 1", (0, 128, 0))
    level2_button = Button(SCREEN_WIDTH//2 - 100, 300,
                           200, 50, "Level 2", (128, 0, 0))

    running = True
    while running:
        screen.fill(BLACK)

        font = pygame.font.Font(None, 74)
        title = font.render("Select Level", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        screen.blit(title, title_rect)

        level1_button.draw(screen)
        level2_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if level1_button.is_clicked(mouse_pos):
                    return 1
                elif level2_button.is_clicked(mouse_pos):
                    return 2


def start_level(level=1, saved_state=None):
    # Play level 2 intro video if starting level 2
    # if level == 2:
    play_video('videos/insert_coin.mp4')

    global bullet_hold_start_time

    player = Player()
    if saved_state:
        player.rect.x, player.rect.y = saved_state["player_pos"]
        player.width, player.height = saved_state["player_size"]
        player.score = saved_state["score"]
        level = saved_state["level"]
        player.resize()

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    bullet_hold_start_time = None
    bullet_max_size = 30

    ADDENEMY = pygame.USEREVENT + 1
    # make level 2 harder, enemies spawn quicker
    spawn_time = 400 if level == 2 else 500
    pygame.time.set_timer(ADDENEMY, spawn_time)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if not pause_game():
                        running = False
                    continue
                elif event.key == K_SPACE and bullet_hold_start_time is None:
                    bullet_hold_start_time = pygame.time.get_ticks()

            elif event.type == KEYUP:
                if event.key == K_SPACE and bullet_hold_start_time is not None:
                    hold_duration = pygame.time.get_ticks() - bullet_hold_start_time
                    bullet_size = min(bullet_max_size, 10 +
                                      hold_duration // 100)
                    bullet = Bullet(player.rect.right, player.rect.centery,
                                    width=bullet_size, height=bullet_size // 2)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
                    bullet_hold_start_time = None

            elif event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.resize(increase=True)
                elif event.button == 3:
                    player.resize(increase=False)

            elif event.type == ADDENEMY:
                new_enemy = Enemy(level)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        bullets.update()
        enemies.update()

        for bullet in bullets:
            enemy_hit = pygame.sprite.spritecollideany(bullet, enemies)
            if enemy_hit:
                enemy_hit.kill()
                bullet.kill()
                player.score += 10

        if level == 1:
            screen.fill((19, 109, 21))
        else:
            screen.fill((150, 75, 0))

        font = pygame.font.Font(None, 36)
        score_text = font.render(
            f'Score: {player.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            save_game(player, level)
            player.die()  # Play explosion sound
            player.kill()
            running = False

        pygame.display.flip()
        clock.tick(30)

    return player.score


def main():
    pygame.display.set_caption("Space Shooter")

    while True:
        choice = show_main_menu()

        if choice == "quit":
            try:
                theme_music.stop()
            except:
                pass
            break
        elif choice == "start":
            start_level(level=1)
        elif choice == "load":
            saved_state = load_game()
            if saved_state:
                start_level(saved_state=saved_state)
            else:
                start_level(level=1)
        elif choice == "level":
            selected_level = show_level_select()
            if selected_level:
                start_level(level=selected_level)

    pygame.quit()


if __name__ == "__main__":
    main()
