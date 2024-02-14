import sys
import pygame
import pygame.camera

pygame.init()
pygame.font.init()

# colors
WHITE = (255, 255, 255)

# main window
WIDTH = 960
HEIGHT = 540
screen = pygame.display.set_mode([WIDTH, HEIGHT])
speed = 5
isJump = False
JUMP_VEL = 20


def mouse_pos():
    return pygame.mouse.get_pos()


def update_fps():
    fps = (str(int(clock.get_fps())))
    font = pygame.font.SysFont("Arial", 18)
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text


# creates object of player
class Player:
    def __init__(self):
        self.width = 25
        self.height = 25
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (WIDTH / 2 - 25 / 2, HEIGHT - 125)
        self.on_ground = False
        self.isJump = False
        self.isDead = False
        self.jump_vel = 0
        self.deaths = 0

    def death(self):
        self.isDead = True
        player.rect.topleft = (WIDTH / 2 - 25 / 2, HEIGHT - 125)
        self.deaths += 1

    def update(self, player_speed, obj_list):

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

        # check for collisions
        for obj in obj_list:
            # check collision in y direction
            if obj.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height) \
                    and not isinstance(obj, EmptyBlock):
                # collision
                # check if collision is an enemy
                x = isinstance(obj, spike)
                if x:
                    player.death()
                # check if below the ground
                if self.jump_vel < 0:
                    dy = obj.rect.bottom - self.rect.top
                    self.jump_vel = 0
                # check if above ground or falling
                elif self.jump_vel >= 0:
                    dy = obj.rect.top - self.rect.bottom

            # check collision in x direction
            elif obj.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height) \
                    and not isinstance(obj, EmptyBlock):
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

    def return_self(self):
        return self


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
        self.object_list = []
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
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def draw(self):
        row_num = 0
        for row in self.world_data:
            for index, val in enumerate(self.world_data[row_num]):
                if val == 1:  # create a block wherever there is a 1
                    self.object_list.append(Block(index * self.width, row_num * self.width, self.width, self.height))
                elif val == 2:
                    self.object_list.append(spike(index * self.width, row_num * self.width, self.width))
                elif val == 0:
                    self.object_list.append(EmptyBlock(index * self.width, row_num * self.width, self.width, self.height))
            row_num += 1


class EmptyMap:
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
                elif val == 0:
                    EmptyBlock(index * self.width, row_num * self.width, self.width, self.height)
            row_num += 1


# creates things
player = Player()
# world initialization
editor_map = EmptyMap()
default_map = Map()

death_count = Text(200, 60, 50, f"{player.deaths}")
death_text = Text(120, 60, 50, "Deaths:")
clock = pygame.time.Clock()

# intro screen creation of things
ready_text = Text(WIDTH / 2, HEIGHT / 2, 100, "READY?")
start_button = Button(WIDTH / 2 - 40, 350, 150, 75)
start_text = Text(start_button.x, start_button.y, start_button.height, "Start")
editor_button = Button(WIDTH / 2 - 40, 430, 300, 75)
editor_text = Text(editor_button.x, editor_button.y, editor_button.height, "Level Editor")

# level select
# four colums each with 5 levels
level1_button = Button(192, 90, 120, 54)
level1_text = Text(level1_button.x, level1_button.y, level1_button.height, "Level 1")
level2_button = Button(192, 180, 120, 54)
level2_text = Text(level2_button.x, level2_button.y, level2_button.height, "Level 2")
editor_level_button = Button(768, 90, 220, 54)
editor_level_text = Text(editor_level_button.x, editor_level_button.y, editor_level_button.height, "Editor Level")


class GameState():
    def __init__(self):
        # scene at start of the game
        self.block_num = 0
        self.state = "intro"

    def main_game(self, level):
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
                if level1_button.mouse_over():
                    default_map.draw()
                    game_state.state = "main_game"
                if level2_button.mouse_over():
                    print("level2 press")
                if editor_level_button.mouse_over():
                    editor_map.draw()
                    game_state.state = "main_game"
            # button press check
            # if event.type == pygame.MOUSEBUTTONUP:

        # white background
        screen.fill((255, 255, 255))

        # button and text display
        level1_button.draw()
        level1_text.update(level1_text.text)
        level2_button.draw()
        level2_text.update(level2_text.text)
        editor_level_button.draw()
        editor_level_text.update(editor_level_text.text)

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
                if editor_button.mouse_over():
                    editor_map.draw()
                    game_state.state = "level_editor"
        # event handling
        # pressed_keys = pygame.key.get_pressed()

        # white background
        screen.fill((255, 255, 255))

        # drawing buttons
        start_button.draw()
        editor_button.draw()

        # drawing text
        ready_text.update(ready_text.text)
        start_text.update(start_text.text)
        editor_text.update(editor_text.text)

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

            # placing blocks
            if event.type == pygame.MOUSEBUTTONDOWN:  # checking if mouse button was pressed
                for obj in obj_list:  # iterating through all objects on map
                    if obj.rect.left < mouse_pos()[0] < obj.rect.right \
                            and obj.rect.top < mouse_pos()[1] < obj.rect.bottom:  # if mouse pos was in an obj when pressed
                        x_index = int(obj.rect.x / 30)
                        y_index = int(obj.rect.y / 30)
                        editor_map.world_data[y_index][x_index] = self.block_num
                editor_map.draw()  # only redraws / updates world if something changed

        # drawing
        screen.fill(WHITE)

        # displaying map
        for obj in obj_list:
            screen.blit(obj.surf, obj.rect)
            pygame.draw.rect(screen, (0, 0, 0), obj.rect, 1)

        # updating the display
        screen.blit(update_fps(), (10, 0))
        pygame.display.update()

    def state_manager(self):
        if self.state == "main_game":
            self.main_game()
        if self.state == "intro":
            self.intro()
        if self.state == "level_editor":
            self.level_editor()
        if self.state == "level_select":
            self.level_select()
        # enter other states of game in here in if statement


# starting game
game_state = GameState()
while True:
    game_state.state_manager()
    clock.tick(60)
