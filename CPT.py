# This program is a choose your own adventure game
# @course ICS3UC
# date 2019/05/31
# @author Henushan Balachandran & Nathaniel Fernandes

import pygame
import random

# Define some colors
R_1 = (237, 59, 68)
R_2 = (252, 95, 95)
B_1 = (55, 167, 242)
B_2 = (104, 197, 255)
Y_1 = (255, 221, 86)
Y_2 = (252, 255, 86)
G_1 = (56, 247, 110)

GREY = (89, 91, 94)
lightGrey = (122, 122, 122)
BLACK    = (   42,   42,   42)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
PI = 3.141592653

lavaColor = [255, 42, 0]

# This not our code, we got it from (https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images)
# This subprogram makes it easier to load images to pygame
# we improved the code for different cases
def load_image(name, opaque, color):

    # if the image is completely opaque
    if opaque:
        image = pygame.image.load(name).convert_alpha()
    else:
        image = pygame.image.load(name).convert()
        image.set_colorkey(color)

    return image


# This sprite acts as the ground for the falling lava, used to check collisions
class floor_rock(pygame.sprite.Sprite):

    #creator 
    def __init__(self, color, width, height):

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()


# falling rocks sprite
class falling_rock(pygame.sprite.Sprite):

    # creator
    def __init__(self, width, height, speed):

        # Call the parent class (Sprite) constructor
        super().__init__()

        # randomizes the height and width of the object
        self.randomNumber = random.randrange(-2, 15)
        width += self.randomNumber * 3
        height += self.randomNumber * 3

        # allows the color of the rocks to be changed
        self.flip = 1
        self.color = [255, random.randint(45, 200), 0]

        # Create an image of the block, and fill it with a color.
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)

        # randomizes the speed of the rocks
        self.speed = speed + self.randomNumber

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    # subprogram to update any changes in the rocks position or color
    def update(self):

        self.rect.y += self.speed

        # make sure the color stays within the right range
        if (self.color[1] > 200):
            self.flip *= -1
        elif (self.color[1] < 40):
            self.flip *= -1

        self.color[1] += self.flip
        self.image.fill(self.color)
    

# player sprite
class player(pygame.sprite.Sprite):

    # creator 
    def __init__(self, color, width, height, speed):

        super().__init__()

        self.image = load_image("player.png", False, WHITE)
        #self.image = pygame.Surface([width, height])
        #self.image.fill(color)

        self.rect = self.image.get_rect()

        self.speed = speed
        self.speed1 = 10
        self.speed2 = 10

    # subprogram to keep the player on the screen
    def collision(self):

        if (self.rect.y > 820):
            self.speed2 = 0
            self.rect.y = 820
        if (self.rect.x >= 1470):
            self.speed1 = 0
            self.rect.x = 1470
        elif (self.rect.x <= 5):
            self.speed1 = 0
            self.rect.x = 5

    # supprgram that simulates a constant gravity on the player
    def gravity(self):

        self.speed2 += 2
        self.rect.y += self.speed

        if (self.rect.y <= 0):
            self.speed2 = self.speed2 * -0.5
            self.rect.y = 5


# class health_bar(pygame.sprite.Sprite):

#     def __init__(self):

#         super().__init__()
#         self.width = 48
#         self.height = 148
#         self.color = [255, 0, 0]
#         #load_iamge("health_bar.png", False, WHITE)
#         self.image = pygame.Surface([self.width, self.height])
#         self.image.fill(self.color)
        
#         self.rect = self.image.get_rect()


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
size = (1500, 1000)

# creates the screen
screen = pygame.display.set_mode(size)

# This is a list of 'sprites.' Each object in the program is
# added to this list. The list is managed by a class called 'Group.'
rock_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()

# This is a list of every sprite.
# All rocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# creates the floor sprite
floor = floor_rock(WHITE, screen.get_width(), 100)
floor.rect.x = 0
floor.rect.y = screen.get_height() + 100

all_sprites_list.add(floor)





# health = health_bar()
# health.rect.x = 1435
# health.rect.y = 20

# healthG = pygame.sprite.Group()
# healthG.add(health)




rock_speed = 5

# subprogram which creates a rock when called
def createRock(speed):

    rock = falling_rock( 60, 60, speed)
    rock.rect.x = random.randrange(0, size[0])
    rock.rect.y = random.randrange(-1*size[1], 0)
    
    rock_list.add(rock)
    all_sprites_list.add(rock)


# creates the player sprite
player1 = player(R_1, 40, 60, 14)
player1.rect.x = 750
player1.rect.y = 800

player_list.add(player1)
all_sprites_list.add(player1)







# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

# this is not our code, we got it from ()
# variables used for allowing the player to jump
jump = False
high = 15
jumpcount = high

# used to create the first set of rocks
initial_rock = True


# used for changing colors
colorFlip = 1


graphics = 1

if (graphics == 1):
    background_image = load_image("background1.png", True, WHITE)
    background_image = pygame.transform.scale(background_image, (1500, 1000))

elif (graphics == 2):
    # loads the background image 
    background_image = load_image("background2.png", False, WHITE)
    background_image = pygame.transform.scale(background_image, (1500, 1000))



health = -144
healthColor = [0, 255, 0]
healthChange = 5
healthColorChange = 10
health_image = load_image("health_bar.png", False, WHITE)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #if (event.type == pygame.KEYDOWN):

    # gets the user key inputs
    keys = pygame.key.get_pressed()


    # player movement

    # lateral movement
    if keys[pygame.K_a]:
        player1.rect.x -= player1.speed
    if keys[pygame.K_d]:
        player1.rect.x += player1.speed

    # this is not our code, we got it from ()
    # allows the player to jump
    if not (jump):
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            jump = True
    else:
        if jumpcount >= -high:
            direction = 1
            if jumpcount < 0:
                direction = -1
            player1.rect.y -= (jumpcount ** 2) * 0.25 * direction
            jumpcount -= 0.5
        else:
            jump = False
            jumpcount = high

    
    if (graphics == 2):
        # used to make the lava in the background image change color
        pygame.draw.rect(screen, lavaColor, [650, 120, 350, 300])

        if (lavaColor[1] > 200):
            colorFlip *= -1
        elif (lavaColor[1] < 1):
            colorFlip *= -1
        lavaColor[1] += colorFlip

    screen.blit(background_image,(0, 0))

    pygame.draw.rect(screen, healthColor, [1435, 168, 48, health])
    screen.blit(health_image, (1435, 20) )

    if (health > 0):
        healthChange = 0
    






    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    # Fetch the x and y out of the list,
       # just like we'd fetch letters out of a string.
    # Set the player object to the mouse location

    # creates the first set of rocks when the game begins
    if initial_rock:
        for i in range(15):
            createRock(rock_speed)
            initial_rock = False

    # See if the player has collided with any rock.
    rock_collisions = pygame.sprite.spritecollide(player1, rock_list, False)

    # See if any rocks have collided with the floor.
    rock_floor = pygame.sprite.spritecollide(floor, rock_list, True)

    # runs for every player-rock collision
    for rock in rock_collisions:
        score += 1
        health += healthChange 

        if (healthColor[1] < 10) or (healthColor[0] > 250):
            healthColorChange = 0
    
        healthColor[0] += healthColorChange 
        healthColor[1] -= healthColorChange 

        print(score)

    # runs for every floor-rock collision
    for rock in rock_floor:
        createRock(rock_speed)
        rock_speed += 0.02

    # calls the update function of each rock
    for rock in rock_list:
        rock.update()

    # calls the gravity and collision for player1
    player1.gravity()
    player1.collision()

    # Draw all the spites
    all_sprites_list.draw(screen)
    #healthG.draw(screen)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
