# Very Simple Gradient:

This is a very simple program that I made in a day just for fun. As the title says, it's a very simple gradient that is written with Python, using Pygame.

It's very simple in that the colour of each pixel on the screen is determined by their distance from three anchor points, representing Red, Green, and Blue. Thus, you cannot interpolate between colours that are not RGB. It's also very simple in that it is very unoptimized - drawing a single gradient on a 1080p screen takes around 5 seconds (when using 3 anchors). It may be improved later, but idk.


# Exeuctable Usage:

If you want to use the program through the executable, then you can simply run it and it will generate a random gradient. Use the S key to screenshot your gradient, the R key ro load a new one, and the Q key to quit the program. As of now, the usage of the executable is more limited.


# Python Usage:

By default, running the program will cause it to create a gradient, where the R, G and B anchor points are all in random places with slightly varying intensity, however you can change this on lines 204 - 206, where the anchor points are instantiated. You can include as many anchor points as you want, as long as they are instantiated with their colour set to either "RED", "GREEN" or "BLUE". Setting it to any other colour will cause a KeyError.

The gradient takes a few seconds to load, and you can see it being created. At any time, you can press the R key delete the current gradient and generate a new one, or press the Q key to quit the program entirely. You can also press the S key to take a screenshot of the gradient, by default this will save to a folder called Gradients in the same directory as the Python file, however you can change the default path by editing a text file in the same directory, called "Default Path"

# Required Packages:

- pygame (pip install pygame)

- glob (pip install glob2)

- screeninfo (pip install screeninfo)


# Sample Gradients:

![](Sample/0.png?raw=true)

![](Sample/1.png?raw=true)

![](Sample/2.png?raw=true)

![](Sample/3.png?raw=true)

# Builds:

- [x] - Windows

- [ ] - Mac

- [x] - Linux
