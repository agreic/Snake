import matplotlib.pyplot as plt
import numpy as np
import random
import keyboard
import time

# Constants
speed = 1  # Pixels per frame
a, b = 10, 10  # Size of borders
initial_size = 1  # Initial size of snake
snake_a, snake_b = 50 , 50  # Initial position of snake
dx, dy = 0, 1  # Direction of snake initially
snake = [np.array([snake_a%a, snake_b%b])]  # Initial position of snake (list of segments)
apple = np.array([random.randint(0, b), random.randint(0, b)])  # Initial position of apple
restart_keys = ['r', 'R']
restart_game = False

plt.ion()
fig, ax = plt.subplots()

# Drawing the initial plot
def draw():
    ax.clear()
    ax.set_xlim(0, a)
    ax.set_ylim(0, b)
    snake_x = [segment[0] for segment in snake]
    snake_y = [segment[1] for segment in snake]
    ax.plot(snake_x, snake_y, 'ro')
    ax.plot(apple[0], apple[1], 'go')
    plt.draw()
    plt.pause(0.05)

draw()

Game = True

def update(snake, apple, size, dx, dy):
    new_head = snake[-1] + np.array([dx, dy])
    new_head[0] %= a
    new_head[1] %= b
    snake.append(new_head)
    if len(snake) > size:
        snake.pop(0)
    if np.array_equal(new_head, apple):
        size += 1
        applea = random.randint(0, a-1)
        appleb = random.randint(0, b-1)
        apple = np.array([applea, appleb])
        while any(np.array_equal(apple, segment) for segment in snake):
                    applea = random.randint(0, a-1)
                    appleb = random.randint(0, b-1)
                    apple = np.array([applea, appleb])
    print('Snake', snake ,'\t', 'Apple', apple, '\t', 'Size', size)
    return snake, apple, size

valid_keys = ['w', 's', 'a', 'd', 'up', 'down', 'left', 'right', 'q']
def wait_for_keypress(valid_keys, wait_time=0.05):
    start_time = time.time()
    while time.time() - start_time < wait_time:
        for key in valid_keys:
            if keyboard.is_pressed(key):
                return key
        time.sleep(0.01)
    return None

def got_key(key, dx, dy):
    if key == 'w' or key == 'up':
        dx, dy = 0, speed
    elif key == 's' or key == 'down':
        dx, dy = 0, -speed
    elif key == 'a' or key == 'left':
        dx, dy = -speed, 0
    elif key == 'd' or key == 'right':
        dx, dy = speed, 0
    return dx, dy

def check_collision(snake):
    for xx in range(len(snake)):
        for yy in range(xx+1, len(snake)):
            if np.array_equal(snake[xx], snake[yy]):
                return True

# Main loop
while True:
    snake = [np.array([50, 50])]  # Initial position of snake (list of segments)
    apple = np.array([random.randint(0, b) - 1, random.randint(0, b) - 1])  # Initial position of apple
    size = initial_size
    dx, dy = 0, 1  # Initial direction
    Game = True
    restart_keys = ['r', 'R']

    while Game:
        snake, apple, size = update(snake, apple, size, dx, dy)
        draw()
        key = wait_for_keypress(valid_keys)
        if key == 'q':
            Game = False
        elif key is not None:
            dx, dy = got_key(key, dx, dy)
        
        time.sleep(0.1)
        if check_collision(snake):
            Game = False
        
        if keyboard.is_pressed('R'):
            restart_game = True
    
    print("Game Over")
    time.sleep(1)
    start_time = time.time()
    wait_time = 10
    while time.time() - start_time < wait_time:
        key = wait_for_keypress(restart_keys)
        if key is not None:
            restart_game = True
            break
    if restart_game:
        continue  # Restart the game by skipping the rest of the code and going back to the beginning of the main loop
    else:
        break  # Exit the main loop if 'R' is not pressed to restart the game

plt.ioff()
plt.show()
