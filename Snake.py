import curses
import random

# --- Main Game Function ---
def main(stdscr):
    # --- Initial Setup ---
    # Hide the cursor
    curses.curs_set(0)
    
    # Get the screen height and width
    sh, sw = stdscr.getmaxyx()
    
    # Create a new window for the game, using the full screen
    window = curses.newwin(sh, sw, 0, 0)
    
    # Allow the window to receive input from the keypad
    window.keypad(1)
    
    # Set the delay for waiting for user input (in milliseconds).
    # This also controls the speed of the snake. Lower is faster.
    window.timeout(100)

    # --- Game State Initialization ---
    # Initial position of the snake's head
    snk_x = sw // 4
    snk_y = sh // 2
    
    # The snake's body, represented as a list of coordinates [y, x]
    # It starts with 3 segments
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    # Initial position of the food
    # We use a character from the ACS set for a nice look
    food = [sh // 2, sw // 2]
    window.addch(food[0], food[1], curses.ACS_PI)

    # Initial direction of the snake
    key = curses.KEY_RIGHT
    
    # Initial score
    score = 0

    # --- Main Game Loop ---
    while True:
        # Get the next key press from the user. It's non-blocking thanks to window.timeout().
        next_key = window.getch()
        
        # If no key is pressed, 'key' remains the same. 
        # If a key is pressed, use it unless it's the reverse direction.
        if next_key != -1:
            if (key == curses.KEY_RIGHT and next_key != curses.KEY_LEFT) or \
               (key == curses.KEY_LEFT and next_key != curses.KEY_RIGHT) or \
               (key == curses.KEY_UP and next_key != curses.KEY_DOWN) or \
               (key == curses.KEY_DOWN and next_key != curses.KEY_UP):
                key = next_key

        # --- Collision Detection ---
        # Check if the snake has hit the wall or itself
        if (snake[0][0] in [0, sh-1] or 
            snake[0][1] in [0, sw-1] or 
            snake[0] in snake[1:]):
            
            # Game over
            curses.endwin() # Restore terminal
            print(f"Game Over! Final Score: {score}")
            quit()

        # --- Calculate New Head Position ---
        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        
        # Add the new head to the front of the snake's body
        snake.insert(0, new_head)

        # --- Food Logic ---
        # Check if the snake has eaten the food
        if snake[0] == food:
            score += 1
            food = None # Mark food as eaten
            while food is None:
                # Generate new food at a random position
                new_food = [
                    random.randint(1, sh - 2),
                    random.randint(1, sw - 2)
                ]
                # Place new food only if it's not on the snake's body
                food = new_food if new_food not in snake else None
            window.addch(food[0], food[1], curses.ACS_PI)
        else:
            # If food is not eaten, remove the last segment of the snake
            # This creates the illusion of movement
            tail = snake.pop()
            window.addch(tail[0], tail[1], ' ')

        # --- Drawing the Game ---
        # Draw the snake's head
        window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
        # Display the score
        window.addstr(0, 2, f"Score: {score}")

# This wrapper handles the setup and teardown of curses
curses.wrapper(main)