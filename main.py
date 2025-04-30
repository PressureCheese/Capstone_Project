# Importing and initializing the neccessary modules.
import pygame
import random
import asyncio
pygame.font.init()
pygame.mixer.init()

# Setting up the screen.
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Target Practice")

# Making a clock variable for time-based events.
clock = pygame.time.Clock()

# Setting up the main background.
background = pygame.image.load("Background.png").convert()

# Setting up the font.
font = pygame.font.Font(None, 50)

# Setting up the restart button.
button_surface = pygame.image.load("Button.png").convert()
button_rect = button_surface.get_rect(center = (500, 600))
button_mask = pygame.mask.from_surface(button_surface)

# Setting up the cursor hitbox.
cursor_surface = pygame.Surface((1, 1)).convert()
cursor_mask = pygame.mask.from_surface(cursor_surface)

# Setting up the red target.
redtarget_surface = pygame.image.load(RedTarget.png").convert_alpha()
redtarget_rect = redtarget_surface.get_rect(midright = (-400, 700))
redtarget_mask = pygame.mask.from_surface(redtarget_surface)

# Setting up the blue target.
bluetarget_surface = pygame.image.load("BlueTarget.png").convert_alpha()
bluetarget_rect = bluetarget_surface.get_rect(midright = (-800, 450))
bluetarget_mask = pygame.mask.from_surface(bluetarget_surface)

# Setting up the yellow target.
yellowtarget_surface = pygame.image.load("YellowTarget.png").convert_alpha()
yellowtarget_rect = yellowtarget_surface.get_rect(midright = (-1600, 100))
yellowtarget_mask = pygame.mask.from_surface(yellowtarget_surface)

# Setting up and playing music.
music = pygame.mixer.Sound("music.mp3")
music.set_volume(.5)
music.play(loops = -1)

# Setting up hit sound effect.
hit_sfx = pygame.mixer.Sound("hit.mp3")
hit_sfx.set_volume(.3)

# INPUT: None
# RETURN: None
# PURPOSE: To run all other functions and code.
async def main():
    # The async is for uploading the game to a web browser.
    # Setting up the game loop.
    running = True
    # Defining miscelaneous variables.
    start = True
    main_game = True
    while running:
        if main_game:
            if start:
                global score
                score = 0
                second_count = 0
                time = 30
                redtarget_rect.x = rng(1)
                bluetarget_rect.x = rng(2)
                yellowtarget_rect.x = rng(3)
                start = False

            mouse_pos = pygame.mouse.get_pos()
            # Checking for player input.
            for event in pygame.event.get():
                # Clicking the red X to exit.
                if event.type == pygame.QUIT:
                    running = False
                
                # Mouse click.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Yellow target clicked.
                    if yellowtarget_mask.overlap(cursor_mask, (mouse_pos[0] - yellowtarget_rect.x, mouse_pos[1] - yellowtarget_rect.y)):
                        score += 5
                        yellowtarget_rect.x = rng(3)
                        hit_sfx.play()
                    # Blue target clicked.
                    elif bluetarget_mask.overlap(cursor_mask, (mouse_pos[0] - bluetarget_rect.x, mouse_pos[1] - bluetarget_rect.y)):
                        score += 2
                        bluetarget_rect.x = rng(2)
                        hit_sfx.play()
                    # Red target clicked.
                    elif redtarget_mask.overlap(cursor_mask, (mouse_pos[0] - redtarget_rect.x, mouse_pos[1] - redtarget_rect.y)):
                        score += 1
                        redtarget_rect.x = rng(1)
                        hit_sfx.play()

            # Displaying the background.
            screen.blit(background, (0, 0))

            # Setting up the score textbox.
            score_surface = font.render(f"Score: {score}", False, "Black")

            # Displaying the score.
            screen.blit(score_surface, (10, 10))

            # Setting up the timer textbox.
            timer_surface = font.render(f"Time: {time}", False, "Black")

            # Displaying the time left.
            screen.blit(timer_surface, (800, 10))

            # Displaying the red target.
            screen.blit(redtarget_surface, redtarget_rect)
            # Moving the red target.
            redtarget_rect.x += 10
            if redtarget_rect.x >= 1160:
                redtarget_rect.x = rng(1)

            # Displaying the blue target.
            screen.blit(bluetarget_surface, bluetarget_rect)
            # Moving the blue target.
            bluetarget_rect.x += 20
            if bluetarget_rect.x >= 1160:
                bluetarget_rect.x = rng(2)

            # Displaying the yellow target.
            screen.blit(yellowtarget_surface, yellowtarget_rect)
            # Moving the yellow target.
            yellowtarget_rect.x += 20
            # Determines direction of up/down movement.
            if yellowtarget_rect.y >= 250:
                direction = False
            if yellowtarget_rect.y <= 100:
                direction = True
            # Executes up/down movement.
            if direction:
                yellowtarget_rect.y += 10
            elif not direction:
                yellowtarget_rect.y -= 10
            if yellowtarget_rect.x >= 1096:
                yellowtarget_rect.x = rng(3)

            # Timer mechanics.
            second_count, time = timer(second_count, time)
            if time == -1:
                main_game = False


            # Updating the screen.
            pygame.display.update()
        
            # Lock fps to 60.
            clock.tick(60)
        
        else:
            # Refreshing start for the next game.

            mouse_pos = pygame.mouse.get_pos()
            # Checking for player input
            for event in pygame.event.get():
                # Clicking on the red X to exit.
                if event.type == pygame.QUIT:
                    running = False
                
                # Mouse click.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_mask.overlap(cursor_mask, (mouse_pos[0] - button_rect.x, mouse_pos[1] - button_rect.y)):
                        start = True
                        main_game = True

            # Displaying the background.
            screen.blit(background, (0, 0))

            # Setting up the final score.
            finalscore_surface = font.render(f"Final score: {score}", False, "Black")
            # Displaying the final score.
            screen.blit(finalscore_surface, (10, 10))

            # Displaying the button surface.
            screen.blit(button_surface, button_rect)

            # Setting up the play again text.
            playagain_surface = font.render("Play Again", False, "Black")
            # Displaying the play again text.
            screen.blit(playagain_surface, (button_rect.x + 39, button_rect.y + 45))

            # Updating the screen.
            pygame.display.update()

            # Lock fps to 60. This isn't necessary, but it may help with CPU usage during the game over screen.
            clock.tick(60)
            
            # Waits 0 seconds for asyncio
            await asyncio.sleep(0)


# INPUT: int
# OUTPUT: int, int
# PURPOSE: To generate a random number based on the parameter given.
def rng(decider):
    if decider == 1:
        rng_num = random.randrange(-1000, -399)
    elif decider == 2:
        rng_num = random.randrange(-3000, -2199)
    elif decider == 3:
        rng_num = random.randrange(-5000, -4199)
    return rng_num

# INPUT: None
# OUTPUT: None
# PURPOSE: To make a timer for the game.
def timer(second_count, time):
    second_count += 1
    if second_count == 60:
        second_count = 0
        time -= 1
    return second_count, time

asyncio.run(main())
