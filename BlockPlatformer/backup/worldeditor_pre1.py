import pygame
from SaveLoadManager import SaveLoadSystem
import sys

pygame.init()

# main window
WIDTH = 960
HEIGHT = 540
screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
speed = 5
isJump = False
JUMP_VEL = 20
font = pygame.font.SysFont("Arial", 18)

saveloadmanager = SaveLoadSystem(".txt")


def update_fps():
    fps = (str(int(clock.get_fps())))
    fps_text = font.render(fps, True, pygame.Color("coral"))
    return fps_text


def level_display(level):
    level_str = str(level)
    level_text = font.render(f"level:{level_str}", True, pygame.Color("coral"))
    return level_text


def text(text):
    text_render = font.render(f"{text}", True, pygame.Color("coral"))
    return text_render


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
                    and not isinstance(obj, EmptyBlock) and not isinstance(obj, Spawn):
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
                    and not isinstance(obj, EmptyBlock) and not isinstance(obj, Spawn):
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


def mouse_pos():
    return pygame.mouse.get_pos()


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
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y)
        obj_list.append(self)


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
                elif val == 0:
                    EmptyBlock(index * self.width, row_num * self.width, self.width, self.height)
                elif val == 3:
                    Spawn(index * self.width, row_num * self.width)
                elif val == 4:
                    Shooter(index * self.width, row_num * self.width, "left", bullet_speed, total_bullets)
            row_num += 1


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


# bullet stats
bullet_speed = 3
total_bullets = 2


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


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x, y+self.height/2)


obj_list = []
player = Player()
editor_map = Map()
editor_map.draw()


class GameState():
    def __init__(self):
        self.level = 1
        self.block_num = 0
        self.bul_list = []
        self.state = "level_editor"

    def level_editor(self):
        pressed_keys = pygame.key.get_pressed()

        # event checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pressed_keys[pygame.K_SPACE]:
                game_state.state = "level_test"
                for obj in obj_list:
                    if isinstance(obj, Spawn):
                        player.rect.x = obj.x
                        player.rect.y = obj.y
            # changing block to be placed
            if pressed_keys[pygame.K_b]:  # block
                self.block_num = 1
            if pressed_keys[pygame.K_s]:  # spike
                self.block_num = 2
            if pressed_keys[pygame.K_p]:  # spawn
                self.block_num = 3
            if pressed_keys[pygame.K_g]:  # shooter
                self.block_num = 4
            if pressed_keys[pygame.K_BACKSPACE]:  # empty block
                self.block_num = 0
            if pressed_keys[pygame.K_UP]:  # up 1 level
                self.level += 1
            if pressed_keys[pygame.K_DOWN]:  # down 1 level
                self.level -= 1
            if pressed_keys[pygame.K_k]:  # save level
                saveloadmanager.save_data(f"level_{self.level}", editor_map.world_data)
            if pressed_keys[pygame.K_l]:  # load level
                try:
                    level_data = saveloadmanager.load_data(f"level_{self.level}.txt")
                    editor_map.world_data = level_data
                except:
                    print(f"level_{self.level} does not exist")

            if event.type == pygame.MOUSEBUTTONDOWN:  # checking if mouse button was pressed
                for obj in obj_list:  # iterating through all objects on map
                    if obj.rect.left < mouse_pos()[0] < obj.rect.right \
                            and obj.rect.top < mouse_pos()[1] < obj.rect.bottom:
                        # if mouse pos was in an obj when pressed
                        obj_list.remove(obj)
                        x_index = int(obj.rect.x / 30)
                        y_index = int(obj.rect.y / 30)
                        print("in")
                        editor_map.world_data[y_index][x_index] = self.block_num
                editor_map.draw()  # only redraws / updates world if something changed
                # drawing
            if self.block_num == 4:  # if shooter is selected
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse = mouse_pos()
                    # calculate which section mouse is in
                    
            screen.fill((255, 255, 255))

            # displaying map
            for obj in obj_list:
                screen.blit(obj.surf, obj.rect)
                pygame.draw.rect(screen, (0, 0, 0), obj.rect, 1)

            screen.blit(level_display(self.level), (50, 0))
            screen.blit(text("L = Load Level"), (120, 0))
            screen.blit(text("K = Save Level"), (250, 0))

            # updating the display
            pygame.display.update()

    def level_test(self):
        pressed_keys = pygame.key.get_pressed()
        # event checker
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pressed_keys[pygame.K_SPACE]:
                game_state.state = "level_editor"

        player.update(speed)

        # drawing
        screen.fill((255, 255, 255))

        # drawing map
        for obj in obj_list:
            screen.blit(obj.surf, obj.rect)
            if isinstance(obj, Shooter):
                self.bul_list = Shooter.shoot(obj)
        for bullet in self.bul_list:
            screen.blit(bullet.surf, bullet.rect)
            if player.rect.colliderect(bullet):
                player.death()

        # draws player
        screen.blit(player.surf, player.rect)

        # fps
        screen.blit(update_fps(), (10, 0))
        screen.blit(level_display(self.level), (50, 0))

        # updating the display
        pygame.display.update()

    def state_manager(self):
        if self.state == "level_editor":
            self.level_editor()
        if self.state == "level_test":
            self.level_test()


game_state = GameState()
while True:
    game_state.state_manager()
    clock.tick(60)
