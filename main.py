import pygame
from pygame.locals import * # Imports the keywords of events that can be used in the game
import time # For the delay in the movement of the block - automatic movement
import random # For moving the apple to different locations

SIZE = 40 # the dimension of the block - in the properties of the image the dimension can be viewed as 40x40
BACKGROUND = (57, 29, 117) # RGB values of background colour

class Apple:
    def __init__(self, game_screen):
        self.apple_score = 0 # Initializing the score value to 0
        self.game_screen = game_screen # Since we need to load the image of apple on the game screen
        self.apple = pygame.image.load("C:/Users/Hp/PycharmProjects/Snake_Game/resources/apple.jpg").convert()  # Accessing the image "apple" in the folder resources
        self.apple_x = 120 # x-coordinate of the apple
        self.apple_y = 120 # y-coordinate of the apple

    def draw_apple(self):
        self.game_screen.blit(self.apple, (self.apple_x, self.apple_y))  # Drawing the image of apple on the game screen at the location apple_x x apple_y
        pygame.display.flip()  # Updates the game screen after a change

    def apple_move(self): # For moving the apple after collision with the snake
        self.apple_x = random.randint(0, 20) * SIZE # A random value is chosen for the x-coordinate
        self.apple_y = random.randint(0, 15) * SIZE # A random value is chosen for the y-coordinate
        self.apple_score += 1 # When the snake eats an apple the score is increased by 1


class Snake:
    def __init__(self, game_screen, length): # __init__ is the constructor for the class Snake. game_screen is the optional arguement.
        self.length = length
        self.game_screen = game_screen # The arguement is assigned to a global variable
        self.block = pygame.image.load("C:/Users/Hp/PycharmProjects/Snake_Game/resources/block.jpg").convert()  # Accessing the image "block" in the folder resources
        #self.block_x = 100  # The x-coordinate for the game starting point - for a single block
        self.block_x = [SIZE] * length # For the length of the snake
        #self.block_y = 100  # The y-coordinate for the game starting point - for a single block
        self.block_y = [SIZE] * length # For the length of the snake
        self.direction = "down"

    def increase_length(self): # Increasing the length of the snake when it eats an apple
        self.length += 1 # The length of the snake is increased by 1
        self.block_x.append(1) # This is done so dat the x and y coordinate will have the proper range for execution in snake.walk()
        self.block_y.append(1)

    def draw_block(self):
        self.game_screen.fill(BACKGROUND)  # Fills the game screen "surface" with any colour of choice - This is like a new screen getting
                                    # displayed at every function call of draw_block() - If this isnt there, there will be a continuous trail of blocks
        for i in range(self.length): # Since there are multiple blocks for loop is used to create a snake of multiple blocks
            self.game_screen.blit(self.block, (self.block_x[i], self.block_y[i]))  # Drawing the image of block on the game screen at the location 250x250
        pygame.display.flip()  # Updates the game screen after a change

    def walk(self, direction):
        self.direction = direction
        # For the movement of the snake - when the snake changes direction, the head moves in the direction and the following blocks-
        # should follow. i.e, the current block occupies the position occupied by the previous block
        for i in range(self.length-1, 0, -1): # The for loop starts iteration from length-1 to 0, reducing by a factor of 1
            self.block_x[i] = self.block_x[i - 1] # x-coordinate of the ith block is equal to the x-coordinate of the i-1th block
            self.block_y[i] = self.block_y[i - 1] # y-coordinate of the ith block is equal to the y-coordinate of the i-1th block

        if self.direction == "up":
            self.block_y[0] -= SIZE # The y-coordinate is reduced by 10
        if self.direction == "down":
            self.block_y[0] += SIZE # The y-coordinate is increased by 10
        if self.direction == "right":
            self.block_x[0] += SIZE  # The x-coordinate is increased by 10
        if self.direction == "left":
            self.block_x[0] -= SIZE # The x-coordinate is reduced by 10
        self.draw_block() # the function draw_block is called to modify the changes

'''
    def move_up(self): # function to move the block up
        self.direction = "up"

    def move_down(self): # function to move the block down
        self.direction = "down"

    def move_right(self): # function to move the block right
        self.direction = "right"

    def move_left(self): # function to move the block left
        self.direction = "left"'''

class Game:
    def __init__(self): # constructor for class Game
        pygame.init() # initializing pygame
        # The self. is given so that the variable surface becomes a class member and can be accessed inside other functions defines inside class
        self.surface = pygame.display.set_mode((900, 700))  # Initializes the game screen
        self.surface.fill(BACKGROUND)  # Fills the game screen "surface" with any colour of choice
        self.snake = Snake(self.surface, 5) # Calling the class and function to draw the snake
        self.snake.draw_block()
        self.apple = Apple(self.surface) # Calling the class and function to draw the apple
        self.apple.draw_apple()

    def score(self):
        font = pygame.font.SysFont('calibiri', 20)
        score = font.render(f"Score:{self.apple.apple_score}", True, (200,200,200))
        self.surface.blit(score, (700,20))


    def game_play(self): # This is done to modularize the function calling for each draw element
        self.snake.game_screen.fill(BACKGROUND)
        self.snake.walk(self.snake.direction)  # Calling the function to initiate the movement of snake
        self.apple.draw_apple()  # Callin the function to display the apple - This is done because the screen is cleared in the function draw_block()
        self.score() # Function call to display score
        pygame.display.flip() # This updates the game screen

        if self.collision(self.snake.block_x[0], self.snake.block_y[0], self.apple.apple_x, self.apple.apple_y) == True:
            self.snake.increase_length() # Function call for increasing the length of the snake
            self.apple.apple_move() # If the snake collides with the apple, the function apple_move() is called

        for i in range(1,self.snake.length): # Checking whether the snake has collided with itself
            # The head of the snake block_x[0] x block_y[0] is colliding with block_x[i] x block_y[i]
            if self.collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i], self.snake.block_y[i]):
                raise "Game over"

    def game_over(self):
        font = pygame.font.SysFont("Calibiri", 40)
        line1 = font.render(f"GAME IS OVER!! Your score is {self.apple.apple_score}", True, (230, 14, 14))
        self.surface.blit(line1, (300, 300))
        line2 = font.render(f"To play again press ENTER. To exit press ESC", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def game_reset(self): # Re-initializing the snake and apple classes for reset
        self.snake = Snake(self.surface, 5)  # Calling the class and function to draw the snake
        self.apple = Apple(self.surface)  # Calling the class and function to draw the apple

    def collision(self, x1, y1, x2, y2): # The function determines the criteria for collision of the snake's head with the apple
        if x1 >= x2 and x1 < x2 + SIZE: # x1 - apple's x coordinate and x2 - snake's x coordinate
            if y1 >= y2 and y1 < y2 + SIZE: # y1 - apple's y coordinate and y2 - snake's y coordinate
                return True

        return False

    def run(self):
        running = True
        game_pause = False # This is for reseting the game

        while running:  # Initiating an infinite loop to retain the game screen
            for event in pygame.event.get():  # pygame.event is the list of inputs the user can give using a keyboard
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  # Press the Esc key to quit the game screen
                        running = False
                    if event.key == K_RETURN: # If the ENTER key is pressed the game resets
                        game_pause = False

                    if game_pause == False: # If the game is over the following keys will not function
                        if event.key == K_UP: # The up-arrow key is pressed to move the block up
                            #self.snake.move_up()
                            self.direction = "up"
                            self.snake.walk(self.direction)
                        if event.key == K_DOWN: # The down-arrow key is pressed to move the block down
                            #self.snake.move_down()
                            self.direction = "down"
                            self.snake.walk(self.direction)
                        if event.key == K_RIGHT: # The right-arrow key is pressed to move the block towards right
                            #self.snake.move_right()
                            self.direction = "right"
                            self.snake.walk(self.direction)
                        if event.key == K_LEFT: # The left-arro`w key is pressed to move the block towards left
                            #self.snake.move_left()
                            self.direction = "left"
                            self.snake.walk(self.direction)

                elif event.type == QUIT:  # To quit the game screen press "Cancel"
                    running = False

            try:
                if game_pause == False: # The game is not over the game_play function is called
                    self.game_play() # This is done to modularize the function calling for each draw element
            except Exception as e:
                game_pause = True # If the game is over, i.e, the snake collided with itself, game_over() is called is message is displayed
                self.game_over()
                self.game_reset() # The game resets

            time.sleep(0.3)

if __name__ == '__main__':
    game = Game()
    game.run()

















