# Os is used solely to remove the pygame start message, nothing else
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Pygame is obviously used to display the shit
import pygame

# Random is used for shuffling a list, and for adding variation into the displaying of columns
import random

# We use glob for managing screenshots
import glob

# Math module is used for distance shit
import math

# Screeninfo so the program can get your monitor size there's prolly a better way idk
from screeninfo import get_monitors

# Getting the user's monitors and initilising Pygame
monitors = get_monitors()
pygame.init()


# The AnchorPoint class just holds some very basic information about the location and colour of the anchor point
class AnchorPoint():
    def __init__(self, colour, pos, intensity):

        # This varaible is not yet used, at the moment it is just for clarifying the intended colour of the AnchorPoint
        self.colour = colour

        # Both pos (a tuple with both x and y) and x/y are collected in order to be more versatile
        self.x = pos[0]; self.y = pos[1]
        self.pos = pos
        self.intensity = intensity


# A function that we use to check if Pygame is being closed by various input methods
def check_close():
    for event in pygame.event.get():

        # Ye if the user closes the pygmae then close it bruv
        if event.type == pygame.QUIT:
            return "Q"

    # If they press R then close and instantly reopen it
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        return "R"

    # IF they press Q then we quit
    if keys[pygame.K_q]:
        return "Q"

    # If the key pressed is 's' then return S
    global can_screenshot
    if keys[pygame.K_s]:
        return "S"

    # Otherwise, allow a screenshot to be taken
    else:
        can_screenshot = True

    # Otherwise we return none
    return "None"


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

    # We have to check that the orientation exists first
    assert h in h_dict; assert v in v_dict

    return (h_dict[h], v_dict[v])


def anchor_dist(object):
    pass


# Function for taking screenshots
def screenshot(win):

    # Made global here because of Syntax shit
    global can_screenshot

    # If we cant take a screenshot then return instantly
    if not can_screenshot:
        return

    # We need it to be a fucking global variable ughhhh
    global number_screenshots

    # Ye
    pygame.image.save(win, f"{PATH}{number_screenshots}.png")
    number_screenshots += 1

    # We play the shutter sound lol
    shutter_sound.play()

    # And then prevent further screenshots from being taken
    can_screenshot = False


# Main function
def main(win, anchors):

    # Defining anchor points for different colours
    RED = anchors[0]
    BLUE = anchors[1]
    GREEN = anchors[2]

    # Nested for loop that draws like a million pixels
    for y in range(win_h):

        for x in range(win_w):

            # Maths to determine the intensity of colour (either R, G or B) based on distance
            red_dist = abs(math.dist((x, y), (RED.pos)) * (max_colour / max_dist) - max_colour) * RED.intensity
            if red_dist >= max_colour:
                red_dist = max_colour

            blue_dist = abs(math.dist((x, y), (BLUE.pos)) * (max_colour / max_dist) - max_colour) * BLUE.intensity
            if blue_dist >= max_colour:
                blue_dist = max_colour

            green_dist = abs(math.dist((x, y), (GREEN.pos)) * (max_colour / max_dist) - max_colour) * GREEN.intensity
            if green_dist >= max_colour:
                green_dist = max_colour

            # Drawing THE pixel
            win.set_at((x, y), (red_dist, green_dist, blue_dist))

        # This percentage chance adds some variation into the drawing of the the window
        if random.randint(0, 100) > 0:
            pygame.display.update()

        # If the user pressed Q, then close the program
        if check_close() == "Q":
            return False

        # If they pressed R then reset it idk
        if check_close() == "R":
            win.fill((0, 0, 0))
            return True

        # If they press S then take a mf screenshot
        if check_close() == "S":

            # We use a function because we epic
            screenshot(win)

    # We need to keep Pygame running even when we're finished drawing, so we have this epic thing right here
    while True:

        # Same shit as above but i have to repeat it
        if check_close() == "Q":
            return False

        if check_close() == "R":
            win.fill((0, 0, 0))
            return True

        if check_close() == "S":
            screenshot(win)

        # There isn't really anything to display at this point but ye
        pygame.display.update()


# We store the path where images should be saved in a text file adjacent to the Python file
path_store = open("Default Path.txt", "r").readlines()
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
shutter_sound = pygame.mixer.Sound('Camera Shutter.wav')
can_screenshot = True

# Funi while loop
while True:

    # List of anchor objects that are passed into the main() function
    anchor_obj = [
        AnchorPoint(colour="RED", pos=(random.randint(0, win_w), random.randint(0, win_h)), intensity=random.uniform(0.8, 1.25)),
        AnchorPoint(colour="BLUE", pos=(random.randint(0, win_w), random.randint(0, win_h)), intensity=random.uniform(0.8, 1.25)),
        AnchorPoint(colour="GREEN", pos=(random.randint(0, win_w), random.randint(0, win_h)), intensity=random.uniform(0.8, 1.25))
    ]

    # Setting the Pygame surface
    window = pygame.display.set_mode((win_w, win_h))

    # Since main() returns either True or False we use that to determine if the Pygame window gets closed
    if not main(window, anchor_obj):
        pygame.quit()
        quit()
