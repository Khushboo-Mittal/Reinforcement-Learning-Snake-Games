import random
import numpy as np
import pickle


class LearnSnake:
    def __init__(self): 
        # Initialize screen dimensions        
        self.screen_width = 600
        self.screen_height = 400
         
        # Set the size of the snake and its speed 
        self.snake_size = 10
        self.snake_speed = 15
        
        # Initialize snake's coordinates and length         
        self.snake_coords = []
        self.snake_length = 1
        # Set initial direction of the snake
        self.dir = "right"
        
        # Create the game board: 
        # A 2D array where 0 means empty cell, 1 means snake is in that cell, and 2 means food is present
        self.board = np.zeros((self.screen_height // self.snake_size, self.screen_width // self.snake_size)) # if a cell contains a 1, it means the snake is in that cell. If a cell contains a 2, it means food is there.
        
        # Flag to indicate if the game is over
        self.game_close = False
        
        # Initialize the starting position of the snake at the center of the screen
        self.x1 = self.screen_width / 2
        self.y1 = self.screen_height / 2
        
        # Convert the snake's coordinates to board indices
        self.r1, self.c1 = self.coords_to_index(self.x1, self.y1)
        # Mark the initial position of the snake on the board
        self.board[self.r1][self.c1] = 1
             
        self.c_change = 1 # Change in column (moving right)
        self.r_change = 0 # Change in row (not moving up or down)
        
        # Generate the initial position of the food and update the board  
        self.food_r, self.food_c = self.generate_food()
        self.board[self.food_r][self.food_c] = 2
        # Initialize the survival counter
        self.survived = 0

        # Call the step function to start the game loop
        self.step()
    
    def get_state(self):
        # Get the coordinates of the snake's head
        head_r, head_c = self.snake_coords[-1]
        
        # Initialize the state list to hold various features
        state = []
        
        # Add the current direction of the snake to the state
        state.append(int(self.dir == "left"))   # Is the snake moving left?
        state.append(int(self.dir == "right"))  # Is the snake moving right?
        state.append(int(self.dir == "up"))     # Is the snake moving up?
        state.append(int(self.dir == "down"))   # Is the snake moving down?
        
        # Add information about the food's position relative to the snake's head
        state.append(int(self.food_r < head_r))  # Is the food above the snake?
        state.append(int(self.food_r > head_r))  # Is the food below the snake?
        state.append(int(self.food_c < head_c))  # Is the food to the left of the snake?
        state.append(int(self.food_c > head_c))  # Is the food to the right of the snake?
        
        # Check if moving in each direction is unsafe and add to the state
        state.append(self.is_unsafe(head_r + 1, head_c))  # Check if moving down is unsafe
        state.append(self.is_unsafe(head_r - 1, head_c))  # Check if moving up is unsafe
        state.append(self.is_unsafe(head_r, head_c + 1))  # Check if moving right is unsafe
        state.append(self.is_unsafe(head_r, head_c - 1))  # Check if moving left is unsafe

        return state  # Return the constructed state list for example : # (0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1)
    
    def is_unsafe(self, r, c):
        # Check if the given coordinates (r, c) are unsafe for the snake to move to
        if self.valid_index(r, c): # Ensure the coordinates are within valid bounds
          if self.board[r][c] == 1: # Check if there's a part of the snake in that cell
              return 1 # Unsafe if the snake occupies the cell
          return 0
        else:
          return 1 # Unsafe if the coordinates are out of bounds
        
    
    # Calculate and return the Euclidean distance between two points (r1, c1) and (r2, c2)
    def get_dist(self, r1, c1, r2, c2):
        return ((r2 - r1) ** 2 + (c2 - c1) ** 2) ** 0.5
        
    # Check if the given indices (r, c) are valid for the board            
    def valid_index(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0])
     
    # Convert the pixel coordinates (x, y) to board indices (r, c)    
    def coords_to_index(self, x, y):
        r = int(y // 10) # Row index based on y coordinate
        c = int(x // 10) # Column index based on x coordinate
        return (r, c)  
    
    # Generate random food coordinates within the bounds of the game board
    def generate_food(self):
        food_c = int(round(random.randrange(0, self.screen_width - self.snake_size) / 10.0))
        food_r = int(round(random.randrange(0, self.screen_height - self.snake_size) / 10.0))
        # Ensure food is generated in an empty cell
        if self.board[food_r][food_c] != 0:
            food_r, food_c = self.generate_food()
        return food_r, food_c #Return the generated food coordinates
    
    def game_over(self):
        return self.game_close
        
        
        
    def step(self, action="None"):
        # If no action is provided, choose a random action (for exploration)
        if action == "None":
            action = random.choice(["left", "right", "up", "down"])
        else:
            action = ["left", "right", "up", "down"][action]
        
        reward = 0
 
        # Update direction and movement based on the chosen action
        if action == "left" and (self.dir != "right" or self.snake_length == 1):
            self.c_change = -1
            self.r_change = 0
            self.dir = "left"
        elif action == "right" and (self.dir != "left" or self.snake_length == 1):
            self.c_change = 1
            self.r_change = 0
            self.dir = "right"
        elif action == "up" and (self.dir != "down" or self.snake_length == 1):
            self.r_change = -1
            self.c_change = 0
            self.dir = "up"
        elif action == "down" and (self.dir != "up" or self.snake_length == 1):
            self.r_change = 1
            self.c_change = 0
            self.dir = "down"

        # Check if the snake has collided with the wall (out of bounds)
        if self.c1 >= self.screen_width // self.snake_size or self.c1 < 0 or self.r1 >= self.screen_height // self.snake_size or self.r1 < 0:
            self.game_close = True
        self.c1 += self.c_change
        self.r1 += self.r_change
        
        # Append the new position of the snake's head to the coordinates list
        self.snake_coords.append((self.r1, self.c1))
        
        if self.valid_index(self.r1, self.c1):
            self.board[self.r1][self.c1] = 1
        
        #removes the last segment of the snake, updating the game board to reflect its new position.
        if len(self.snake_coords) > self.snake_length:
            rd, cd = self.snake_coords[0]
            del self.snake_coords[0]
            if self.valid_index(rd, cd):
                self.board[rd][cd] = 0
 
        #if the head of the snake has collided with any of its body segments, which results in a game over.
        for r, c in self.snake_coords[:-1]:
            if r == self.r1 and c == self.c1:
                self.game_close = True
 
 
        if self.c1 == self.food_c and self.r1 == self.food_r: # if the snake's head has reached the food
            self.food_r, self.food_c = self.generate_food() # generates new food
            self.board[self.food_r][self.food_c] = 2 #updates the board
            self.snake_length += 1 #increases the snake's length
            reward = 1 # food eaten, so +1 reward
        else:
            rh1, ch1 = self.snake_coords[-1] #current position of the snake's head,
            if len(self.snake_coords) == 1:
                rh2, ch2 = rh1, ch1 #If the snake has just one segment, it sets rh2 and ch2 to the head's position.
            else:
                rh2, ch2 = self.snake_coords[-1] #assigns the head's position to rh2 and ch2.
        
        # death = -10 reward
        if self.game_close:
            reward = -10
        self.survived += 1 #number of survived steps is still counted, indicating how long the snake lasted before losing.
        
        return self.get_state(), reward, self.game_close
            
        
    # run game using given episode (from saved q tables)
    # no visual - just returns snake length
    
    def run_game(self, episode):
        # Construct the filename for loading the Q-table from a pickle file based on the episode number
        filename = f"pickle/{episode}.pickle"
        with open(filename, 'rb') as file:
            table = pickle.load(file)
        current_length = 2
        steps_unchanged = 0
        
        # Continue the game until the game is over
        while not self.game_over():
            state = self.get_state()
            action = np.argmax(table[state])
            if steps_unchanged == 1000: # Break the loop if the snake's length hasn't changed for 1000 steps
                break
            self.step(action) # Execute the chosen action
            
            # Check if the snake's length has changed
            if self.snake_length != current_length:
                steps_unchanged = 0 # Reset the unchanged steps counter if the snake has grown
                current_length = self.snake_length # Update the current length to the new length
            else:
                steps_unchanged += 1 
                
        return self.snake_length
            
        