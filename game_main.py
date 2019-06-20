import pygame
from game_sprites import *


class FighterGame(object):
    """Fighter Game main"""

    def __init__(self):
        # print("Initializing the Game...")

        # 1. Create the game window 
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. Create the game clock 
        self.clock = pygame.time.Clock()
        # 3. Call private method to create the game sprites and sprite groups
        self.__create_sprites()

        # 4. Set the timer event for creating the Enemy Sprite　1 Enemy Sprite/1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
		# 5. Set the timer event for creating the Bullet Sprite 1 Bullet Sprite per 0.5s
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    def __create_sprites(self):

        # Create the Background Sprite and Group 
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # Create the Enemy Fighter Sprite and Group
        self.enemy_group = pygame.sprite.Group()

        # Create the Hero Fighter Sprite and Group 
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("Game starts...")

        while True:
            # 1. Set the refresh frequency 60 frames per second
            self.clock.tick(FRAME_PER_SEC)
            # 2. Listen to the events
            self.__event_handler()
            # 3. Check the collision of different Sprite Groups
            self.__check_collide()
            # 4. Update and draw the Sprite Groups
            self.__update_sprites()
            # 5. Update the screen
            pygame.display.update()

    def __event_handler(self):

        for event in pygame.event.get():

            # Check if quit the game 
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # Create the Enemy Fighter Sprite
                enemy = Enemy()
                # Add the Enemy Fighter Sprite to the Group
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # Get the keyboard event to move the Hero Fighter Sprite 
        keys_pressed = pygame.key.get_pressed()
        # Check the different keyboard event
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -2
        else:
            self.hero.speed = 0

    def __check_collide(self):

        # 1. The Bullet Sprite collided with the Enemy Fighter Sprite
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)

        # 2. The Enemy Fighter Sprite collided with the Hero Fighter Sprite 
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # Check the Hero Fighter Sprite collided with the Enemy Fighter Sprite
        if len(enemies) > 0:

            # Remove the Hero Fighter Sprite 
            self.hero.kill()

            # Call the game_over method to end
            FighterGame.__game_over()

    def __update_sprites(self):
	
		# Update the Background Sprite Group
        self.back_group.update()
        self.back_group.draw(self.screen)

		# Update the Enemy Fighter Sprite Group
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

		# Update the Hero Fighter Sprite Group
        self.hero_group.update()
        self.hero_group.draw(self.screen)

		# Update the Bullet Sprite Group
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        print("Game Over")

        pygame.quit()
        exit()

if __name__ == '__main__':

    # Create the game object
    game = FighterGame()

    # Start the game
    game.start_game()
