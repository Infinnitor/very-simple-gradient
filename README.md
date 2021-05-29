# Very Simple Gradient

This is a very simple program that I made in a day just for fun. As the title says, it's a very simple gradient that is created using Pygame.

It's very simple in that the colour of each pixel on the screen is determined by their distance from three anchor points, representing Red, Green, and Blue. Thus, you cannot interpolate between colours that are not RGB. It's also very simple in that it is very unoptimized - drawing a single gradient on a 1080p screen takes around 5 seconds. It may be improved later, but idk.

# Usage

To use the program, you will need a couple modules: Pygame - which is used to display and create the gradient, and Screeninfo - which is used to get the size of the monitor in order to maximise the display

By default, running the program will cause it to create a gradient, where the R, G and B anchor points are all in random places with slightly varying intensity, however you can change this on lines 204 - 206, where the anchor points are instantiated.

The gradient takes a few seconds to load, and you can see it created in real time. At any time, you can press the R key delete the current gradient and generate a new one, or press the Q key to quit the program entirely. You can also press the S key to take a screenshot of the gradient, by default this will save to a folder called Gradients in the same directory as the Python file, however you can change the default path by editing a text file in the same directory, called "Default Path"


# Future Updates:

At the moment this program is very simple, however I would like to expand it a bit, here are some plans I have:

[ ] Adding the ability for more than three anchors to be present

[ ] More colours to act as anchor points (that aren't just RGB)

[ ] Optimizing the program so that it can generate faster
