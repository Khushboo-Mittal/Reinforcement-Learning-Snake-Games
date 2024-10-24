# import random
# import pygame

# class Apple:
#     def __init__(self, gameDisplay, display_width, display_height, block_size, snake_list):
#         self.gameDisplay = gameDisplay
#         self.block_size = block_size
#         self.width_blocks = display_width // block_size
#         self.height_blocks = display_height // block_size
#         self.update_apple_pos(snake_list)

#     def update_apple_pos(self, snake_list):
#         self.x = random.randint(0, self.width_blocks - 1) * self.block_size
#         self.y = random.randint(0, self.height_blocks - 1) * self.block_size
#         while [self.x, self.y] in snake_list:
#             self.x = random.randint(0, self.width_blocks - 1) * self.block_size
#             self.y = random.randint(0, self.height_blocks - 1) * self.block_size

#     def get_apple_pos(self):
#         return self.x, self.y

#     def display(self):
#         pygame.draw.rect(self.gameDisplay, (255, 0, 0), [self.x, self.y, 10, 10])


# class Snake:
#     def __init__(self, gameDisplay, display_width, display_height, block_size):
#         self.gameDisplay = gameDisplay
#         self.snake_list = [[70, 70]]
#         self.snake_length = 1
#         self.block_size = block_size
#         self.eaten = False
#         self.direction = "right"

#     def is_alive(self):
#         head = self.snake_list[-1]
#         # Check for collisions with walls
#         if not (0 <= head[0] < 150 and 0 <= head[1] < 150):
#             return False
#         # Check for collisions with self
#         if head in self.snake_list[:-1]:
#             return False
#         return True

#     def get_state(self, apple_pos):
#         head = self.snake_list[-1]
#         return [head[0] - apple_pos[0], head[1] - apple_pos[1]]

#     def move(self):
#         head = self.snake_list[-1]
#         if self.direction == "up":
#             new_head = [head[0], head[1] - self.block_size]
#         elif self.direction == "down":
#             new_head = [head[0], head[1] + self.block_size]
#         elif self.direction == "left":
#             new_head = [head[0] - self.block_size, head[1]]
#         elif self.direction == "right":
#             new_head = [head[0] + self.block_size, head[1]]

#         # Update the snake's body
#         self.snake_list.append(new_head)
#         if len(self.snake_list) > self.snake_length:
#             del self.snake_list[0]  # Remove the tail

#     def grow(self):
#         self.snake_length += 1  # Increase the length of the snake

#     def display(self):
#         for segment in self.snake_list:
#             pygame.draw.rect(self.gameDisplay, (0, 255, 0), [segment[0], segment[1], self.block_size, self.block_size])


# def main():
#     pygame.init()  # Initialize Pygame
#     display_width, display_height = 150, 150  # Set display dimensions
#     block_size = 10  # Size of each block
#     gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display window
#     pygame.display.set_caption('Snake Game')  # Set window title

#     clock = pygame.time.Clock()  # Create a clock object to control the frame rate
#     snake = Snake(gameDisplay, display_width, display_height, block_size)  # Initialize Snake
#     apple = Apple(gameDisplay, display_width, display_height, block_size, snake.snake_list)  # Initialize Apple

#     game_running = True  # Game running flag
#     while game_running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:  # Quit if the close button is clicked
#                 game_running = False
#             if event.type == pygame.KEYDOWN:  # Handle key presses for direction
#                 if event.key == pygame.K_LEFT:
#                     snake.direction = "left"
#                 elif event.key == pygame.K_RIGHT:
#                     snake.direction = "right"
#                 elif event.key == pygame.K_UP:
#                     snake.direction = "up"
#                 elif event.key == pygame.K_DOWN:
#                     snake.direction = "down"

#         # Game logic (move snake, check for collisions, etc.)
#         # Update snake position, check for apple, etc.

#         gameDisplay.fill((0, 0, 0))  # Clear the screen with black background
#         apple.display()  # Draw the apple
#         snake.display()  # Draw the snake
#         pygame.display.flip()  # Update the display

#         clock.tick(10)  # Control the frame rate (10 frames per second)

#     pygame.quit()  # Quit Pygame when the loop ends


# if __name__ == "__main__":
#     main()  # Start the game

import random
import pygame

class Apple:
    def __init__(self, gameDisplay, display_width, display_height, block_size, snake_list):
        self.gameDisplay = gameDisplay
        self.block_size = block_size
        self.update_apple_pos(snake_list)

    def update_apple_pos(self, snake_list):
        self.x = random.randint(0, 14) * 10
        self.y = random.randint(0, 14) * 10
        while [self.x, self.y] in snake_list:
            self.x = random.randint(0, 14) * 10
            self.y = random.randint(0, 14) * 10

    def get_apple_pos(self):
        return self.x, self.y

    def display(self):
        pygame.draw.rect(self.gameDisplay, (255, 0, 0), [self.x, self.y, 10, 10])

class Snake:
    def __init__(self, gameDisplay, display_width, display_height, block_size):
        self.gameDisplay = gameDisplay
        self.snake_list = [[70, 70]]
        self.snake_length = 1
        self.block_size = block_size
        self.direction = "right"

    def is_alive(self):
        head = self.snake_list[-1]
        # Check for collisions with walls
        if not (0 <= head[0] < 150 and 0 <= head[1] < 150):
            return False
        # Check for collisions with self
        if head in self.snake_list[:-1]:
            return False
        return True

    def get_state(self, apple_pos):
        head = self.snake_list[-1]
        # State now includes: relative position to apple, danger in directions, and current direction
        return [
            head[0] - apple_pos[0],  # X distance to apple
            head[1] - apple_pos[1],  # Y distance to apple
            int(self.is_danger_ahead()),
            int(self.is_danger_left()),
            int(self.is_danger_right()),
            self.direction
        ]

    def is_danger_ahead(self):
        head = self.snake_list[-1]
        if self.direction == "up" and (head[1] - self.block_size < 0 or [head[0], head[1] - self.block_size] in self.snake_list):
            return True
        if self.direction == "down" and (head[1] + self.block_size >= 150 or [head[0], head[1] + self.block_size] in self.snake_list):
            return True
        if self.direction == "left" and (head[0] - self.block_size < 0 or [head[0] - self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "right" and (head[0] + self.block_size >= 150 or [head[0] + self.block_size, head[1]] in self.snake_list):
            return True
        return False

    def is_danger_left(self):
        head = self.snake_list[-1]
        if self.direction == "up" and (head[0] - self.block_size < 0 or [head[0] - self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "down" and (head[0] + self.block_size >= 150 or [head[0] + self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "left" and (head[1] + self.block_size >= 150 or [head[0], head[1] + self.block_size] in self.snake_list):
            return True
        if self.direction == "right" and (head[1] - self.block_size < 0 or [head[0], head[1] - self.block_size] in self.snake_list):
            return True
        return False

    def is_danger_right(self):
        head = self.snake_list[-1]
        if self.direction == "up" and (head[0] + self.block_size >= 150 or [head[0] + self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "down" and (head[0] - self.block_size < 0 or [head[0] - self.block_size, head[1]] in self.snake_list):
            return True
        if self.direction == "left" and (head[1] - self.block_size < 0 or [head[0], head[1] - self.block_size] in self.snake_list):
            return True
        if self.direction == "right" and (head[1] + self.block_size >= 150 or [head[0], head[1] + self.block_size] in self.snake_list):
            return True
        return False

    def move(self):
        head = self.snake_list[-1]
        if self.direction == "up":
            new_head = [head[0], head[1] - self.block_size]
        elif self.direction == "down":
            new_head = [head[0], head[1] + self.block_size]
        elif self.direction == "left":
            new_head = [head[0] - self.block_size, head[1]]
        elif self.direction == "right":
            new_head = [head[0] + self.block_size, head[1]]

        # Update the snake's body
        self.snake_list.append(new_head)
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]  # Remove the tail

    def grow(self):
        self.snake_length += 1  # Increase the length of the snake

    def display(self):
        for segment in self.snake_list:
            pygame.draw.rect(self.gameDisplay, (0, 255, 0), [segment[0], segment[1], self.block_size, self.block_size])
