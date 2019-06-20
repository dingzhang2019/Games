import random
import pygame

# Set the measurement of screen
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# Set the refresh frequency 1/60 second
FRAME_PER_SEC = 60
# Set the timer event for enemy fighter 
CREATE_ENEMY_EVENT = pygame.USEREVENT
# set the firing bullet event for the Hero fighter
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """Base game sprite class"""

    def __init__(self, image_name, speed=1):

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Define the basic attributes
		# Load the Sprite image 
        self.image = pygame.image.load(image_name)
		# Get the measurement of the Sprite 
        self.rect = self.image.get_rect()
		# Set the moving speed of the Sprite
        self.speed = speed

    def update(self):

        # Move the Sprite upward on the screen
        self.rect.y += self.speed


class Background(GameSprite):
    """Backgroup Sprite class"""

    def __init__(self, is_alt=False):

        # 1. Call the parent class (GameSprite) constructor(image/rect/speed)
        super().__init__("./images/background.png")

        # 2. Check the image is an alternative image and set its initial location
        if is_alt:
            self.rect.y = -self.rect.height
			
	# overide the parent update method to meet the background movement animation
    def update(self):

        # 1. Call the parent update method
        super().update()

        # 2. Check if the Background Sprite has moved out of the screen, if true, reset the location of Background Sprite. 
		#    We use the same background image to move together to get the animation result
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    """Enemy Fighter Sprite"""

    def __init__(self):

        # 1. Call the parent class (GameSprite) constructor
        super().__init__("./images/enemy1.png")

        # 2. Set the random speed of the Enemy Fighter Sprite, 1 ~ 3
        self.speed = random.randint(1, 3)

        # 3. Set the random initial location of the Enemy Fighter Sprite
        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):

        # 1. Call the parent update method to move the Enemy Fighter Sprite upward 
        super().update()

        # 2. Check if the Enemy Fighter Sprite has moved out of the screen, if true, remove it from the Enemy Sprite Group to release the resources
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()

    def __del__(self):
        pass


class Hero(GameSprite):
    """Hero Fighter Sprite"""

    def __init__(self):

        # 1. Call the parent (GameSprite) construtor to set the image and speed
        super().__init__("./images/me1.png", 0)

        # 2. Set the initial location of the Hero Fighter Sprite 
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 3. Create the Bullet Sprite Group
        self.bullets = pygame.sprite.Group()

    def update(self):

        # Move the Hero Fighter Sprite horizontally 
        self.rect.x += self.speed

        # Control the Hero fighter Sprite within the screen
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        #print("Firing...")
		
		# Fire 3 bullets in a row
        for i in range(3):
            # 1. Create the Bullet Sprite
            bullet = Bullet()

            # 2. Set the initial location of the Bullet Sprite
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx

            # 3. Add the Bullet Sprite to the Bullet Sprite Group
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """Bullet Sprite"""

    def __init__(self):

        # Call the parent (GameSprite) constructor to set the image and speed,
		# Set the speed to -2, meaning the bullet moves upward and different speed can be applied
        super().__init__("./images/bullet1.png", -2)

    def update(self):

        # Call the parent update method to move the Bullet Sprite upward
        super().update()

        # Check if the Bullet Sprite has moved out of screen, if true, remove it from the Bullet Sprite Group
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        # print("Bullet has been removed...")
		pass 
