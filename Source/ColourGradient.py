import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Pygame is obviously used to display stuff
import pygame

# Random is used for shuffling a list, and for adding variation into the displaying of columns
import random

# Glob used for managing screenshots
import glob

# Math module is used for distance shit
import math

# Screeninfo so the program can get your monitor size
from screeninfo import get_monitors

# Getting the user's monitors and initilising Pygame
monitors = get_monitors()
pygame.init()


def fix_path(rel_p):
    abs_path = os.path.abspath(rel_p)

    if sys.platform == "win32":
        abs_path = abs_path.replace("/", "\\")
    else:
        abs_path = abs_path.replace("\\", "/")

    return abs_path


# The AnchorPoint class just holds some very basic information about the location and colour of the anchor point
class anchor_point():
    def __init__(self, colour, pos, intensity):

        # Make the colour uppercase, just in case (haha)
        colour = colour.upper()

        # List of RGB colours, used for assigning a random colour, or checking if a colour is valid
        rgb_colours = ("RED", "GREEN", "BLUE")

        # If a random colour was requested, then set the anchor point's colour to a random choice from the RGB list
        if colour == "RANDOM":
            self.colour = random.choice(rgb_colours)

        # Otherwise, make sure that the colour entered was valid, and then assign then anchor point's colour
        else:
            assert colour in rgb_colours, f"{colour} is not an RGB colour, please pick either RED, GREEN, or BLUE"
            self.colour = colour

        self.x = pos[0]; self.y = pos[1]
        self.pos = pos
        self.intensity = intensity


# Update different potential inputs to pygame
def check_close():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "Q"

    # If they press R then close and instantly reopen it
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        return "R"

    # IF they press Q then quit
    if keys[pygame.K_q]:
        return "Q"

    # If the key pressed is 's' then return S
    global can_screenshot
    if keys[pygame.K_s]:
        return "S"

    # Otherwise, allow a screenshot to be taken
    else:
        can_screenshot = True

    # Otherwise return empty string
    return ""


# Function that converts an orientation into actual numbers
def orientate(h, v):

    h_dict = {
        "Center" : round(win_w / 2),
        "Left" : 0,
        "Right" : win_w
    }

    v_dict = {
        "Center" : round(win_h / 2),
        "Top" : 0,
        "Bottom" : win_h
    }

    assert h in h_dict, f"{h} is not a valid orientation"; assert v in v_dict, f"{v} is not a valid orientation"

    return (h_dict[h], v_dict[v])


# Function for taking screenshots
def screenshot(win):

    # Made global here because of Syntax shit
    global can_screenshot

    # If screenshot cannot be taken return instantly
    if not can_screenshot:
        return

    global number_screenshots

    # Ye
    pygame.image.save(win, f"{PATH}{number_screenshots}.png")
    number_screenshots += 1

    shutter_sound.play()
    can_screenshot = False  # You can only take on screenshot per gradient


# Main function
def main(win, anchors):

    # Function for finding the average distance from anchor points of a certain colour
    def anchor_average(anchors):

        # If there are no anchor points in the given list, return 0 instantly to prevent a ZeroDivisionError
        if len(anchors) == 0:
            return 0

        # Defining of all the colour distances from anchors
        anchors_dist = []

        # For loop goes through every anchor in the input list
        for a in anchors:

            # Maths to determine the intensity of colour (either R, G or B) based on distance
            a_dist = abs(math.dist((x, y), (a.pos)) * (max_colour / max_dist) - max_colour) * a.intensity

            # If the colour is too powerful, then cap it at 255
            if a_dist >= max_colour:
                a_dist = max_colour

            # Add the colour intensity to the anchors_dist list
            anchors_dist.append(a_dist)

        # Return the average of the anchors_dist list
        return sum(anchors_dist) / len(anchors_dist)

    # Nested for loop that draws like a million pixels
    for y in range(win_h):

        for x in range(win_w):

            # Finding the average distance from each colour, by using a list of all anchor points of that colour
            RED = anchor_average(anchors["RED"])
            GREEN = anchor_average(anchors["GREEN"])
            BLUE = anchor_average(anchors["BLUE"])

            # Drawing THE pixel
            win.set_at((x, y), (RED, GREEN, BLUE))

        # This percentage chance adds some variation into the drawing of the the window
        if random.randint(0, 100) > 0:
            pygame.display.update()

        # If the user pressed Q, then close the program
        if check_close() == "Q":
            return False

        # If they pressed R then reset it
        if check_close() == "R":
            win.fill((0, 0, 0))
            return True

        # If they press S then take a screenshot
        if check_close() == "S":
            screenshot(win)

    # Mainloop to continue displaying
    while True:
        if check_close() == "Q":
            return False

        if check_close() == "R":
            win.fill((0, 0, 0))
            return True

        if check_close() == "S":
            screenshot(win)

        # There isn't really anything to display at this point but ye
        pygame.display.update()


# Store the path where images should be saved in a text file adjacent to the Python file
path_store = open(fix_path("DefaultPath.txt"), "r").readlines()
PATH = path_store[0].replace("PATH: ", "").replace("\\", "\\\\").replace("\n", "")

# If the Default Path hasn't been defined, then print a warning
if not PATH.replace(" ", ""):
    input("Warning: Path for storing screenshots is not defined! [press enter to continue]")
else:
    # number_screenshots variable for keeping track of the number of screenshots that have been taken, uses glob module to load all png files
    source_images = glob.glob(f"{PATH}*.png")
    number_screenshots = len(source_images)

# Defining variables that control window size and the max range of colours
win_w = monitors[0].width
win_h = monitors[0].height
max_colour = 255
max_dist = math.dist([0, 0], [win_w, win_h])

# Shutter sound effect lol
shutter_sound = pygame.mixer.Sound(fix_path("CameraShutter.wav"))
can_screenshot = True

# Funi while loop
while True:

    # List of anchor objects that are passed into the main() function
    anchor_obj = [
        anchor_point(colour="RANDOM", pos=(random.randint(0, win_w), random.randint(0, win_h)), intensity=random.uniform(0.8, 1.25)),
        anchor_point(colour="RANDOM", pos=(random.randint(0, win_w), random.randint(0, win_h)), intensity=random.uniform(0.8, 1.25)),
        anchor_point(colour="RANDOM", pos=(random.randint(0, win_w), random.randint(0, win_h)), intensity=random.uniform(0.8, 1.25))
    ]

    # Adding the anchors to the anchor dict
    anchor_dict = {"RED" : [], "GREEN" : [], "BLUE" : []}
    for a in anchor_obj:
        anchor_dict[a.colour].append(a)

    # Setting the Pygame surface
    window = pygame.display.set_mode((win_w, win_h))

    # Since main() returns either True or False use that to determine if the Pygame window gets closed
    if not main(window, anchor_dict):
        pygame.quit()
        sys.exit()
