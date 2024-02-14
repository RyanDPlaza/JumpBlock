import sys
import pygame
from SaveLoadManager import SaveLoadSystem
import pygame.camera

pygame.init()
pygame.font.init()

saveloadmanager = SaveLoadSystem(".txt")

# colors
WHITE = (255, 255, 255)

# main window
WIDTH = 960
HEIGHT = 540
screen = pygame.display.set_mode([WIDTH, HEIGHT])
speed = 5
isJump = False
JUMP_VEL = 20
obj_list = []


def mouse_pos():
    return pygame.mouse.get_pos()


def update_fps():
    fps = (str(int(clock.get_fps())))
    font = pygame.font.SysFont("Arial", 18)
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text


def load_level(level_name):
    obj_list.clear()
    try:
        level_data = saveloadmanager.load_data(level_name)
        default_map.world_data = level_data
    except:
        print("level does not exist")
    default_map.draw()
    for obj in obj_list:
        if isinstance(obj, Spawn):
            player.rect.x = obj.x
            player.rect.y = obj.y
    game_state.state = "main_game"


# creates object of player
class Player:
    def __init__(self):
        self.spawn_x = WIDTH / 2
        self.spawn_y = HEIGHT / 2

        self.width = 25
        self.height = 25
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (self.spawn_x, self.spawn_y)  # spawn of player
        self.on_ground = False
        self.isJump = False
        self.isDead = False
        self.jump_vel = 0
        self.deaths = 0

    def death(self):
        self.isDead = True
        player.rect.topleft = (self.spawn_x, self.spawn_y)
        self.deaths += 1

    def update(self, player_speed):
        pressed_keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # jumping code
        if pressed_keys[pygame.K_UP] and not self.isJump and self.on_ground:
            self.isJump = True
            self.jump_vel = -15
        if not pressed_keys[pygame.K_UP]:
            self.isJump = False

        # movement to the left
        if pressed_keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                dx -= speed
        # movement to the right
        if pressed_keys[pygame.K_RIGHT]:
            if self.rect.right < WIDTH - speed:
                dx += speed
        # gravity
        self.jump_vel += 1
        if self.jump_vel > 10:
            self.jump_vel = 10
        dy += self.jump_vel

        # check for collisions with obj list itmes
        for obj in obj_list:
            # check collision in y direction
            if obj.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height) \
                    and not isinstance(obj, EmptyBlock) and not isinstance(obj, Spawn) and not isinstance(obj, Goal):
                # collision
                # check if collision is an enemy
                x = isinstance(obj, spike)
                if x:
                    player.death()
                # check if below the ground9
                if self.jump_vel < 0:
                    dy = obj.rect.bottom - self.rect.top
                    self.jump_vel = 0
                # check if above ground or falling
                elif self.jump_vel >= 0:
                    dy = obj.rect.top - self.rect.bottom

            # check collision in x direction
            elif obj.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height) \
                    and not isinstance(obj, EmptyBlock) and not isinstance(obj, Spawn) and not isinstance(obj, Goal):
                # check if collision is an enemy
                x = isinstance(obj, spike)
                if x:
                    player.death()
                # collision from the right
                if self.rect.x > obj.rect.x:
                    dx = obj.rect.right - self.rect.left
                # collision from the left
                elif self.rect.x < obj.rect.x:
                    dx = obj.rect.left - self.rect.right

            if isinstance(obj, Spawn):
                self.spawn_x = obj.x
                self.spawn_y = obj.y

        # check if on the ground
        if dy == 0:
            self.on_ground = True
        else:
            self.on_ground = False

        # update player movment
        if not self.isDead:
            self.rect.move_ip(dx, 0)
            self.rect.move_ip(0, dy)
        else:
            self.isDead = False


# floating block class
class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 100, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)


class Spawn:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 120))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)


class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)


class spike:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = 30
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((150, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)


class EmptyBlock:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)


# bullet stats
bullet_speed = 3
total_bullets = 20


class Shooter:
    def __init__(self, x, y, direction, bul_speed, total_bul):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.direction = direction
        self.bul_speed = bul_speed
        self.total_bul = total_bul
        self.bul_list = []
        self.bul_count = 0
        self.timer = 0
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((180, 235, 52))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)

    def shoot(self):
        # timer
        self.timer += 1
        # return list of all bullets to be blit
        for bullet in self.bul_list:
            if bullet.rect.x < 0 or bullet.rect.x > WIDTH:  # check if any bullets are offscreen
                self.bul_list.remove(bullet)  # if a bullet is offscreen remove from list
                self.bul_count -= 1

        if self.bul_count < self.total_bul and self.timer > 60:  # if there is room for a new bullet and timer is up
            self.bul_list.append(Bullet(self.x, self.y))  # create new bullet add to list
            self.bul_count += 1  # add 1 to bullet count
            self.timer = 0  # reset timer

        # move every bullet in direction by speed
        for bullet in self.bul_list:
            if self.direction == "right":  # bullets shooting right
                bullet.rect.x += self.bul_speed
            elif self.direction == "left":  # bullets shooting left
                bullet.rect.x -= self.bul_speed

        return self.bul_list

    def update_direction(self, updated_direction):
        self.direction = updated_direction


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y + self.height / 2)


class Button:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((99, 187, 242))
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.surf, self.rect)
        self.mouse_over()

    def mouse_over(self):
        if self.rect.left < mouse_pos()[0] < self.rect.right and self.rect.top < mouse_pos()[1] < self.rect.bottom:
            self.surf.fill((50, 147, 242))
            return True
        else:
            self.surf.fill((99, 187, 242))
            return False


class Text:
    def __init__(self, x, y, font_size, text):
        self.text = str(text)
        self.x = x
        self.y = y
        self.font_size = font_size
        self.font = pygame.font.SysFont("Agency FB", self.font_size)
        self.text_surf = self.font.render(text, True, (0, 0, 0))
        self.text_width, self.text_height = self.text_surf.get_width(), self.text_surf.get_height()

    def update(self, text):
        self.text = str(text)
        self.text_surf = self.font.render(text, True, (0, 0, 0))
        screen.blit(self.text_surf, (self.x - (self.text_width / 2), self.y - (self.text_height / 2)))


# creating the map
# tile size = 30x30
# width = 32
# height = 18
# world.world_data = saveloadmanager.load_data("world_data")
class Map:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.world_data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def draw(self):
        row_num = 0
        for row in self.world_data:
            for index, val in enumerate(self.world_data[row_num]):
                if val == 1:  # create a block wherever there is a 1
                    Block(index * self.width, row_num * self.width, self.width, self.height)
                elif val == 2:
                    spike(index * self.width, row_num * self.width, self.width)
                elif val == 3:
                    Spawn(index * self.width, row_num * self.width)
                elif val == 4:
                    Shooter(index * self.width, row_num * self.width, "right", bullet_speed, total_bullets)
                elif val == 5:
                    Goal(index * self.width, row_num * self.width)
                elif val == 0:
                    EmptyBlock(index * self.width, row_num * self.width, self.width, self.height)
            row_num += 1

    def clear(self):
        self.world_data = []


# creates things

player = Player()
# world initialization
default_map = Map()
default_map.draw()

death_count = Text(200, 60, 50, f"{player.deaths}")
death_text = Text(120, 60, 50, "Deaths:")
clock = pygame.time.Clock()

# intro screen creation of things
ready_text = Text(WIDTH / 2, HEIGHT / 2, 100, "READY?")
start_button = Button(WIDTH / 2 - 40, 350, 150, 75)
start_text = Text(start_button.x, start_button.y, start_button.height, "Start")

# win state text
win_text = Text(WIDTH / 2, HEIGHT / 2, 200, "You WIN!")
continue_text = Text(WIDTH / 2, 450, 50, "SPACE to Continue")

# level select
# two colums each with 5 levels
level1_button = Button(192, 90, 120, 54)
level1_text = Text(level1_button.x, level1_button.y, level1_button.height, "Level 1")
level2_button = Button(192, 180, 120, 54)
level2_text = Text(level2_button.x, level2_button.y, level2_button.height, "Level 2")
level3_button = Button(192, 270, 120, 54)
level3_text = Text(level3_button.x, level3_button.y, level3_button.height, "Level 3")
level4_button = Button(192, 360, 120, 54)
level4_text = Text(level4_button.x, level4_button.y, level4_button.height, "Level 4")
level5_button = Button(192, 450, 120, 54)
level5_text = Text(level5_button.x, level5_button.y, level5_button.height, "Level 5")


class GameState():
    def __init__(self):
        # scene at start of the game
        self.block_num = 0
        self.state = "intro"
        self.bul_list = []

    def main_game(self):
        pressed_keys = pygame.key.get_pressed()
        # event checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pressed_keys[pygame.K_ESCAPE]:
                game_state.state = "intro"

        player.update(speed)

        # drawing
        screen.fill(WHITE)
        death_text.update(death_text.text)
        death_count.update(str(player.deaths))

        # drawing map
        for obj in obj_list:
            if isinstance(obj, Shooter):
                self.bul_list = obj.shoot()
            if isinstance(obj, Goal):
                if player.rect.colliderect(obj):
                    # win code here
                    game_state.state = "win_state"
            for bullet in self.bul_list:
                screen.blit(bullet.surf, bullet.rect)
                if player.rect.colliderect(bullet):
                    player.death()
            screen.blit(obj.surf, obj.rect)

        # draws player
        screen.blit(player.surf, player.rect)

        # fps
        screen.blit(update_fps(), (10, 0))

        # updating the display
        pygame.display.update()

    def level_select(self):
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pressed_keys[pygame.K_ESCAPE]:
                game_state.state = "intro"
            if event.type == pygame.MOUSEBUTTONUP:
                # level select
                # LEVEL 1
                if level1_button.mouse_over():
                    load_level("level_1.txt")
                # LEVEL 2
                if level2_button.mouse_over():
                    load_level("level_2.txt")
                # LEVEL 3
                if level3_button.mouse_over():
                    load_level("level_3.txt")
                # LEVEL 4
                if level4_button.mouse_over():
                    load_level("level_4.txt")
                # LEVEL 5
                if level5_button.mouse_over():
                    load_level("level_5.txt")
            # button press check
            # if event.type == pygame.MOUSEBUTTONUP:

        # white background
        screen.fill((255, 255, 255))

        # button and text display
        level1_button.draw()
        level1_text.update(level1_text.text)
        level2_button.draw()
        level2_text.update(level2_text.text)
        level3_button.draw()
        level3_text.update(level3_text.text)
        level4_button.draw()
        level4_text.update(level4_text.text)
        level5_button.draw()
        level5_text.update(level5_text.text)

        # update display
        pygame.display.update()

    def intro(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # button press check
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.mouse_over():
                    game_state.state = "level_select"
        # event handling
        # pressed_keys = pygame.key.get_pressed()

        # white background
        screen.fill((255, 255, 255))

        # drawing buttons
        start_button.draw()

        # drawing text
        ready_text.update(ready_text.text)
        start_text.update(start_text.text)

        # update display
        pygame.display.update()

    def level_editor(self):
        pressed_keys = pygame.key.get_pressed()
        # event checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pressed_keys[pygame.K_ESCAPE]:
                game_state.state = "intro"
            # changing block to be placed
            if pressed_keys[pygame.K_b]:
                self.block_num = 1
            if pressed_keys[pygame.K_s]:
                self.block_num = 2
            if pressed_keys[pygame.K_BACKSPACE]:
                self.block_num = 0

            if event.type == pygame.MOUSEBUTTONDOWN:  # checking if mouse button was pressed
                for obj in obj_list:  # iterating through all objects on map
                    if obj.rect.left < mouse_pos()[0] < obj.rect.right \
                            and obj.rect.top < mouse_pos()[
                        1] < obj.rect.bottom:  # if mouse pos was in an obj when pressed
                        x_index = int(obj.rect.x / 30)
                        y_index = int(obj.rect.y / 30)
                        default_map.world_data[y_index][x_index] = self.block_num
                default_map.draw()  # only redraws / updates world if something changed

        # drawing
        screen.fill(WHITE)

        # displaying map
        for obj in obj_list:
            screen.blit(obj.surf, obj.rect)
            pygame.draw.rect(screen, (0, 0, 0), obj.rect, 1)

        # updating the display
        screen.blit(update_fps(), (10, 0))
        pygame.display.update()

    def win_state(self):
        pressed_keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pressed_keys[pygame.K_SPACE]:
                game_state.state = "level_select"

            # button press check

        # event handling
        # pressed_keys = pygame.key.get_pressed()

        # white background
        screen.fill((255, 255, 255))

        # drawing text
        win_text.update(win_text.text)
        continue_text.update(continue_text.text)

        # update display
        pygame.display.update()

    def state_manager(self):
        if self.state == "main_game":
            self.main_game()
        if self.state == "intro":
            self.intro()
        if self.state == "level_select":
            self.level_select()
        if self.state == "win_state":
            self.win_state()
        # enter other states of game in here in if statement


# starting game
game_state = GameState()
while True:
    game_state.state_manager()
    clock.tick(60)
