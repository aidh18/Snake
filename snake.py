import arcade
import random



SCREEN_WIDTH = 1240
SCREEN_HEIGHT = 920



# Call game and arcade class
def main():
    game = Game()
    arcade.run()



# Class that defines a block
class Block:

    def __init__(self):
        self.x = random.randrange(0, SCREEN_WIDTH, 40)
        self.y = random.randrange(0, SCREEN_WIDTH, 40)
        self.change_x = 0
        self.change_y = 0
        self.width = 40
        self.height = 40
        self.color = arcade.color.RUFOUS
        self.speed = 10


# Class that defines the Snake game
class Game(arcade.Window):
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake")
        self.fruit = Block()
        self.fruits = []

        self.body_segments = []

        self.head = Block()
        init_head(self.head)
        self.head.speed = 10
        self.head.has_moved = False

        self.score = 0
        self.lose = False
        
        self.user_difficulty = [100, 2, False]
        self.speed_limit = self.user_difficulty[0]
        self.speed_scaling_factor = self.user_difficulty[1]

    

    # Function that defines what should happen on users key press    
    def on_key_press(self, key, modifiers):
        control_head(key, self.head)



    # Function that defines what happens when the mouse is clicked
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.user_difficulty[2]:
            self.user_difficulty = determine_difficulty(x, y)
            self.speed_limit = self.user_difficulty[0]
            self.speed_scaling_factor = self.user_difficulty[1]



    # Function that defines what happens to update the game
    def update(self, delta_time):
        add_new_fruits(self.fruits)
        fruit_eaten = eat_fruits(self.head, self.fruits)
        self.head.speed = set_speed(fruit_eaten, self.head.speed, self.speed_limit, self.speed_scaling_factor)
        move_head(self.head)
        loop_segment(self.head)
        move_body(self.body_segments, self.head)
        grow_body(self.body_segments, fruit_eaten, self.head)
        self.lose = crash_snake(self.head, self.body_segments, self.lose)
        snake_lose(self.lose, self.head, self.body_segments)
        self.set_update_rate(1 / self.head.speed)
        self.score = get_score(fruit_eaten, self.score)
        


        
    # Function that defines what should be drawn on the screen
    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.HONEYDEW)
        if not self.user_difficulty[2]:
            draw_start_buttons()
            draw_start_text()
        else:
            draw_body(self.body_segments)
            draw_fruit(self.fruits)
            draw_head(self.head)
            draw_loss(self.lose, self.score)
            draw_score(self.score, self.lose)
        


# Function that defines how to draw the head when the game starts
def init_head(head):
    head.x = SCREEN_WIDTH / 2
    head.y = SCREEN_HEIGHT / 2
    head.change_x = 40
    head.change_y = 0
    head.width = 40
    head.height = 40
    head.color = arcade.color.MSU_GREEN



# Function that defines when to add new fruits and how to draw those fruits
def add_new_fruits(fruits):
    if len(fruits) < 1:
        fruit = Block()
        fruit.x = random.randrange(20, SCREEN_WIDTH, 40)
        fruit.y = random.randrange(20, SCREEN_HEIGHT, 40)
        fruit.change_x = 0
        fruit.change_y = 0
        fruit.width = 40
        fruit.height = 40
        fruits.append(fruit)



# Function that receives user key presses and moves the head of the snake 
# accordingly
def control_head(key, head):
    if head.has_moved:
        if head.change_y == 0:
            if key == arcade.key.W:
                head.change_y = 40
                head.change_x = 0
                head.has_moved = False
            elif key == arcade.key.S:
                head.change_y = -40
                head.change_x = 0
                head.has_moved = False
        if head.change_x == 0:
            if key == arcade.key.A:
                head.change_x = -40
                head.change_y = 0
                head.has_moved = False
            if key == arcade.key.D:
                head.change_x = 40
                head.change_y = 0
                head.has_moved = False



# Function that checks to see if the snake has run into itself
def crash_snake(head, body_segments, lose):
    for segment in body_segments:
        # check if head is overlapping them
        overlapping = not(
            head.x < segment.x or
            head.x > segment.x or
            head.y < segment.y or
            head.y > segment.y
        )
        
        if overlapping:
            lose = True
        
    return lose



# Function that defines how the difficulty is received from the user
def determine_difficulty(x, y):
    user_difficulty = [100, 2, False]
    difficulty_chosen = False
    x = int(round(x))
    y = int(round(y))
    if x > (SCREEN_WIDTH / 2) - 350 and x < (SCREEN_WIDTH / 2) - 50 and y > (SCREEN_HEIGHT / 2) - 50 and y < (SCREEN_HEIGHT / 2) + 50:
        speed_limit = 20
        speed_scaling_factor = 1.005
        difficulty_chosen = True
    if x > (SCREEN_WIDTH / 2) + 50 and x < (SCREEN_WIDTH / 2) + 350 and y > (SCREEN_HEIGHT / 2) - 50 and y < (SCREEN_HEIGHT / 2) + 50:
        speed_limit = 30
        speed_scaling_factor = 1.008
        difficulty_chosen = True
    if x > (SCREEN_WIDTH / 2) - 350 and x < (SCREEN_WIDTH / 2) - 50 and y > (SCREEN_HEIGHT / 2) - 200 and y < (SCREEN_HEIGHT / 2) - 100:
        speed_limit = 50
        speed_scaling_factor = 1.012
        difficulty_chosen = True
    if x > (SCREEN_WIDTH / 2) + 50 and x < (SCREEN_WIDTH / 2) + 350 and y > (SCREEN_HEIGHT / 2) - 200 and y < (SCREEN_HEIGHT / 2) - 100:
        speed_limit = 70
        speed_scaling_factor = 1.02
        difficulty_chosen = True

    if difficulty_chosen:
        user_difficulty[0] = speed_limit
        user_difficulty[1] = speed_scaling_factor
        user_difficulty[2] = difficulty_chosen

    return user_difficulty



# Function that draws the body of the snake
def draw_body(body_segments):
    for body_segment in body_segments:
        arcade.draw_rectangle_filled(body_segment.x, body_segment.y, body_segment.width, body_segment.height, body_segment.color)


 
# Function that draws the difficulty buttons on start
def draw_start_buttons():
    arcade.draw_rectangle_filled(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2, 300, 100, arcade.color.DARK_GREEN)
    arcade.draw_text("Easy", (SCREEN_WIDTH / 2 - 260), (SCREEN_HEIGHT / 2) - 20, arcade.color.WHITE, font_size = 40)
    arcade.draw_rectangle_filled((SCREEN_WIDTH / 2) + 200, SCREEN_HEIGHT / 2, 300, 100, arcade.color.DARK_GREEN)
    arcade.draw_text("Medium", (SCREEN_WIDTH / 2) + 105, (SCREEN_HEIGHT / 2) - 20, arcade.color.WHITE, font_size = 40)
    arcade.draw_rectangle_filled((SCREEN_WIDTH / 2) - 200, (SCREEN_HEIGHT / 2) - 150, 300, 100, arcade.color.DARK_GREEN)
    arcade.draw_text("Hard", (SCREEN_WIDTH / 2) - 260, (SCREEN_HEIGHT / 2) - 170, arcade.color.WHITE, font_size = 40)
    arcade.draw_rectangle_filled((SCREEN_WIDTH / 2) + 200, (SCREEN_HEIGHT / 2) - 150, 300, 100, arcade.color.DARK_GREEN)
    arcade.draw_text("Insane", (SCREEN_WIDTH / 2) + 120, (SCREEN_HEIGHT / 2) - 170, arcade.color.WHITE, font_size = 40)



# Function that draws the welcoming text
def draw_start_text():
    arcade.draw_text("Welcome to Snake!", (SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT * 0.75, width = 1000, align = "center", color = arcade.color.DARK_JUNGLE_GREEN, font_size = 75, bold = True)
    arcade.draw_text("Choose your difficulty:", (SCREEN_WIDTH / 2) - 500, (SCREEN_HEIGHT * 0.75) - 100, width = 1000, align = "center", color = arcade.color.DARK_JUNGLE_GREEN, font_size = 50, bold = True)



# Function that draws the fruits
def draw_fruit(fruits):
    for fruit in fruits:
        arcade.draw_rectangle_filled(fruit.x, fruit.y, fruit.width, fruit.height, fruit.color)



# Function that draws the fruit
def draw_head(head):
    arcade.draw_rectangle_filled(head.x, head.y, head.width, head.height, head.color)



# Function that draws the loss on the screen
def draw_loss(lose, score):
    if lose:
        arcade.draw_text("YOU CRASHED!", (SCREEN_WIDTH / 2) - 500, SCREEN_HEIGHT * 0.75, width = 1000, align = "center", color = arcade.color.DARK_JUNGLE_GREEN, font_size = 75, bold = True)
        arcade.draw_text(f"Final Score: {score}", (SCREEN_WIDTH / 2) - 525, SCREEN_HEIGHT * 0.75 - 200, width = 1000, align = "center", color = arcade.color.DARK_JUNGLE_GREEN, font_size = 50, bold = True)



# Function that draws the score
def draw_score(score, lose):
    if not lose:
        score_text = f"Score: {score}"
        arcade.draw_text(score_text, start_x = 10, start_y = 50, width = 100, align = "center", font_size = 20, bold = True, color = arcade.color.DARK_JUNGLE_GREEN)



# Function that defines when the snake eats and removes the fruit
def eat_fruits(head, fruits):
    fruit_eaten = []

    eating = not(
        head.x < fruits[0].x or
        head.x > fruits[0].x or
        head.y < fruits[0].y or
        head.y > fruits[0].y
    )
    
    if eating:
        fruit_eaten.append(fruits[0])
    
    for fruit in fruit_eaten:
        fruits.remove(fruit)

    return fruit_eaten



# Function that counts and returns the score
def get_score(fruit_eaten, score):
    for _ in fruit_eaten:
        score += 1
    
    return score



# Function that grows the body as the fruit is eaten
def grow_body(body_segments, fruit_eaten, head):
    for _ in fruit_eaten:

            # Get prior position of last body segment
        if len(body_segments) > 0:
            end_segment = body_segments[-1]
        else:
            end_segment = head

        prior_change_x = end_segment.change_x * -1
        prior_change_y = end_segment.change_y * -1
        prior_x = end_segment.x + prior_change_x
        prior_y = end_segment.y + prior_change_y

        # Create new segment in place of last one
        body_segment = Block()
        body_segment.change_x = end_segment.change_x
        body_segment.change_y = end_segment.change_y
        body_segment.x = prior_x
        body_segment.y = prior_y
        body_segment.width = 40
        body_segment.height = 40
        body_segment.color = arcade.color.MUGHAL_GREEN
        body_segments.append(body_segment)



# Function that allows the snake to loop to the other side when the snake goes off the screen
def loop_segment(segment):
    SIZE_SEGMENT = 40

    if (segment.x - segment.width / 2 + SIZE_SEGMENT) <= 0:
        if segment.change_x <= 0:
            segment.x = SCREEN_WIDTH - segment.width / 2

    if (segment.x + segment.width / 2 - SIZE_SEGMENT) >= SCREEN_WIDTH:
        if segment.change_x >= 0:
            segment.x = 0 + segment.width / 2

    if (segment.y - segment.height / 2 + SIZE_SEGMENT) <= 0:
        if segment.change_y <= 0:
            segment.y = SCREEN_HEIGHT - segment.height / 2
    
    if (segment.y + segment.height / 2 - SIZE_SEGMENT) >= SCREEN_HEIGHT:
        if segment.change_y >= 0:
            segment.y = 0 + segment.height / 2



# Function that defines how the head should move and returns an output when the 
# head has moved
def move_head(head):
    head.x += head.change_x
    head.y += head.change_y
    head.has_moved = True



# Function that defines how the body should follow the head
def move_body(body_segments, head):
    if len(body_segments) > 0:
        
        for segment in body_segments:
            segment.x += segment.change_x
            segment.y += segment.change_y
            loop_segment(segment)

        for i in reversed(range(len(body_segments))):
            trailing_seg = body_segments[i]
            previous_seg = body_segments[i - 1]
            trailing_seg.change_x = previous_seg.change_x
            trailing_seg.change_y = previous_seg.change_y


        body_segments[0].change_x = head.change_x
        body_segments[0].change_y = head.change_y



# Function that determines and sets the speed
def set_speed(fruit_eaten, speed, speed_limit, speed_scaling_factor):
        for _ in fruit_eaten:
            if speed <= speed_limit:
                speed **= speed_scaling_factor
        return speed



# Function that defines how the snake loses and the output that occurs
def snake_lose(lose, head, body_segments):
    if lose:
        head.change_x = 0
        head.change_y = 0

        for segment in body_segments:
            segment.change_x = 0
            segment.change_y = 0

        loss_text = "YOU LOSE"
        
        arcade.draw_text(loss_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, width = 500, align = "center", color = arcade.color.DARK_JUNGLE_GREEN)



# Defines main
def main():
    game = Game()
    arcade.run()



# Calls main and starts the game!
if __name__ == "__main__":
    main()