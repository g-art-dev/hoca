# hoca: an Higher-Order Cellular Automata Python Library

## Overview

In the 80's many computer science magazines featured articles on Conway's game of life and Wolfram's elementary 
cellular automata. Many of these articles told us that cellular automata would revolutionize the arts and sciences.
There have indeed been some interesting scientific developments, but we cannot say that this announcement turned out
to be premonitory, at least for the arts.

`hoca` is a work in progress which aims to provide a framework to test ideas around the use of higher-order
cellular automata to manipulate or create images. It is born while having some artistic goal in mind, but the
approach quickly led to compare it with some traditional algorithms of the image processing toolkit.
So this work is double bound to visual arts and computer science.

`Hoca` is a Python library, and its code was primarily written with readability before speed in mind. So relax
and enjoy the scenery.

## Installation
The latest version of `hoca` is installed via a standard pip command:

```shell
pip install hoca
```

## Documentation

All the code is documented and largely commented, and we strongly recommend taking a look at it.
However, in the following lines, we will introduce some concepts and present some examples.
But this matter could always be enhanced, so feel free to send us any comment, suggestion or question.

### Concepts

`hoca` relies on three concepts provided as classes and their subclasses: The fields, the populations, and
the automata.  
Fields hold the data processed by the automata population - a collection of agents - while populations
orchestrate the global behaviour of the automata.

#### Field classes

The `Field` abstract class (in the `hoca.core.automata_framework` module) provides a common set of definitions of
a field implementation. At the moment, there is only one implementation provided, the `ImageField`
subclass (in the `hoca.core.ImageField` module) that allows image manipulation.

Fields are data structures that hold the source data processed by an automata population,
or the result data produced by them. Fields can also be both source and result at the same time,
this way the automata can modify the field _in place_.  

For this purpose fields have an io_mode property that defines if they are:  
- readable: `io_mode == Field.IOMode.IN`
- writable: `io_mode == Field.IOMode.OUT`
- readable and writable: `io_mode == Field.IOMode.INOUT`

The `ImageField` class provides two convenience class methods:
- `from_image()` that creates an ImageField instance from an image file,
- `blank()` that creates an ImageField filled with zeros.

Once a field (or multiple ones) has been instantiated, it has to be packed in a Python dictionary before
being passed to the automata population. The key used along with the field will serve to select the data
to be read or written by the automata, and to name the logged data.

To facilitate the preparation of the necessary field(s) to be supplied to an automata population, one may
call the `build_field_dict()` class method that all the automata classes must provide.

#### Population classes

The `Population` abstract class (in the `hoca.core.automata_framework` module) provides a minimal set
of definitions of the necessary methods for the automata population operation. The implementation of
these methods is provided in the `BasicPopulation` class (in the `hoca.core.BasicPopulation` module).

`BasicPopulation` offers two main methods:
- `run()` which runs all the automata once (i.e. one generation),
- `play()` which runs all the automata for multiple generations.

The first is the most _complex_ of the two as `play()` simply calls `run()` repeatedly.

`BasicPopulation` implements every features needed to achieve some task with a population of automata
(or at least the features we wanted to investigate), and it's quite easy to use:

1. Build a dictionary referencing one or more fields,
   
2. instantiate a `BasicPopulation` passing the field dictionary and an automata class to it,
   
3. play the population for a while.

The result of the automata process will be in the fields and that's maybe all one wants. However, to have
a clearer view on what's going on with the automata population or for debugging purpose, `hoca` provides
a `BasicPopulation` subclass: The `CallbackPopulation` (in the `hoca.monitor.CallbackPopulation` module).

The `CallbackPopulation` works the same as the `BasicPopulation` but it allows providing callbacks that are
invoked at the end of each generation (more on that below). These callbacks can log some information about
the state of the population or build a video of the movements of the automata.

#### Automata class

The `Automata` abstract class (in the `hoca.core.automata_framework` module) defines the methods all
automaton classes must implement. There are three important methods:

- The `build_field_dict()` class method is responsible for building a well-formed field dictionary in order
  for the automata of this class to be able to process the data they contain. The field dictionary will be
  passed to the population later on.
  
- The `run()` method defines the behaviour of each automaton instance of the implemented `Automaton`
  class. The `run()` method is in charge of:
  - Moving the automaton, and
  - updating the field(s).
  
- The `get_status()` method computes and returns the current status of the automaton. This method will be
  invoked on each generation for each automaton.
  
### Getting started with hoca

The `hoca.demo.LiteEdgeAutomaton` module provides the `LiteEdgeAutomaton` automata class. These automata
crawl an `ImageField` containing an image, and fill another `ImageField` with the contours found 
in the first.

![Edward Hopper. Nighthawks, 1942. The Art Institute of Chicago.](https://github.com/g-art-dev/hoca/raw/main/images/EdwardHopper_Nighthawks_1942.jpg)
> Edward Hopper. Nighthawks, 1942. (CC0) The Art Institute of Chicago.  
> [https://www.artic.edu/artworks/111628/nighthawks](https://www.artic.edu/artworks/111628/nighthawks)  
> (_source field_)

We will now see how to write some code to use this class: We have to build a field dictionary
to:

1. provide the source image and receive the contours drawn,
   
2. constitute a population of `LiteEdgeAutomaton`,

3. and then _play_ the population.
   
Here is the code:

```python
import random

from hoca.core.BasicPopulation import BasicPopulation
from hoca.demo.LiteEdgeAutomaton import LiteEdgeAutomaton

# It may be of some interest to init the pseudo random generator to get consistent result
# across multiple runs. This is optional.
random.seed('This is the seed')

# Build the field
field_dict = LiteEdgeAutomaton.build_field_dict('images/EdwardHopper_Nighthawks_1942.jpg')

# Create the automata population
automata_count = 3800
automata_population = BasicPopulation(field_dict, automata_count, LiteEdgeAutomaton)

# Play the population
automata_population.play(stop_after=2700)

# Display the result
field_dict["result"].image.show()
```

Obviously, the code starts with the importation of the stuff it will need, it then initializes the field
dictionary. In order to do that, the code calls the `build_field_dict()` convenience class method of the automata
class, passing the image to process to it. In this case, the returned dictionary contains two items the
`"source"` field and the `"result"` field.  
Note the parameters of `build_field_dict()` may change from class to class as the data to be processed may
differ.

The automata population is created by instantiating the `BasicPopulation` class. The program passes the field
dictionary, the number of automata to instantiate and the class of the automata to it.
The population is then played for 2700 generations by calling the `play()` method. 

The program ends displaying the result field as an image. The field dictionary may also be accessed through the
corresponding property of the population instance (here `automata_population.field_dict`).

![Nighthawks contours](https://github.com/g-art-dev/hoca/raw/main/images/LiteEdgeAutomation_A3800_I2700_result.jpg)
> Hopper's Nighthawks after 2700 generations with 3800 LiteEdgeAutomaton automata.  
> (_result field_)

As the image representation of a field is a PIL Image class instance, it can be saved or manipulated in many
ways. See the [Pillow Image module documentation](https://pillow.readthedocs.io/en/stable/reference/Image.html)
for more information.

In the previous program, one can see the number of automata to instantiate or the number of generations as kind
of magic numbers.
These numbers depend on the job the automata are doing, or the data provided. For instance, these numbers have
probably to be increased if the source image is larger. 
In the case of the `LiteEdgeAutomaton`, these numbers are discussed in [1].

#### Let's make a video

The `CallbackPopulation` class allows doing various tasks at each generation. For instance, we can aggregate
the result field at each generation to produce a video showing the effect of an automata population on a
source field:

```python
import random

from hoca.demo.LiteEdgeAutomaton import LiteEdgeAutomaton
from hoca.monitor.CallbackPopulation import *

# It may be of some interest to init the pseudo random generator to get consistent result
# across multiple runs. This is optional.
random.seed('This is the seed')

# Build the field
field_dict = LiteEdgeAutomaton.build_field_dict('images/EdwardHopper_Nighthawks_1942.jpg')

# Create the automata population
automata_count = 3800
stop_after = 2700
automata_population = CallbackPopulation(field_dict, automata_count, LiteEdgeAutomaton)

# Register the callbacks...
# A logging callback
automata_population.register_callback(LogProgressCallback(automata_population))
# A video building callback
# video is built from the result fields each 5 generations
automata_population.register_callback(
    SaveFieldsVideoCallback(automata_population,
                            activation_condition_function=Callback.condition_each_n_generation(5)))

# Play the population
automata_population.play(stop_after=stop_after)
```

This code is quite similar to the previous one. But after having initialized the population class, some
callbacks are registered before playing the population. These callbacks are instances
of one of the abstract `Callback` subclass (all defined in the `hoca.monitor.CallbackPopulation` module):

- `LogProgressCallback` logs the progress of the computation in a file or to the console.

- `SaveFieldsImageCallback` and `SaveFieldsVideoCallback` save the fields manipulated by the automata
  population as a collection of images (stored in a folder) or as a video. 

- `SaveTracesImageCallback` or `SaveTracesVideoCallback` save the trace - the positions and/or the trajectories -
  of the automata population as a collection of images (stored in a folder) or as a video. These are
  particularly useful to debug an automaton code.

These callbacks must receive the population as a parameter. They are called on every generation but they can
also receive an optional so-called activation function (or an activation function generator) in order
to control when the callback will have to do its job.
For instance, this mechanism could be used to make the callback aggregate some data at each generation but
only report a summary once in a while.
The activation function will take the population as parameter and return `True` if some condition has
occurred (and `False` otherwise).
In the above example, `Callback.condition_each_n_generation(5)` is a function generator which builds an
activation function returning `True` every 5 generations. Hence, the video produced will have `2700 / 5`
frames (it's 21.6s at 25fps).

We may add the following lines to trace the trajectories of the automata:

```python
    # A callback tracing the automata trajectories
    automata_population.register_callback(
        SaveTracesImageCallback(automata_population,
                                trace=Trace.TRAJECTORIES,
                                activation_condition_function=Callback.condition_at_generation(stop_after)))
```

### Coding an automaton

Writing the code of an automaton needs to take care of few important things. We will illustrate the whole
process by describing the important elements of an automata class and writing a toy arty automata class. 

An automata class must inherit the `Automaton` abstract class and implement some mandatory methods:

- `build_field_dict()` class method. This method will be used to build a proper field dictionary for the
  automaton we are writing. The field dictionary will contain one or more fields. The number of fields depends
  on what the automata are processing. The name (or keys as they're stored in a Python dictionary) can be
  chosen freely.
  
- `run()` instance method. This method will contain the code controlling the behaviour of the automaton.
  It will be called on each generation by the class that handles the automata population (presumably 
  `BasicPopulation` or `CallbackPopulation`). It will have to:
  
  - Read the value at the current automaton position of any provided input (or input-output) field.
    However, please note that nothing prevents the automaton to read the value at any other coordinates.
  
  - Write the value at the current automaton position of any provided output (or input-output) field.
    The same remark as reading the input field(s) applies, the writing can occur anywhere.
    
  - Update the state of the automaton.
  
  - Move the automaton to an adjacent field position. But as before, nothing prevents the automaton to jump
    anywhere.
  
  These tasks may be done in any order (compatible with the purpose of the automaton). Some of them can be omitted
  if they aren't necessary. 
  
- `get_status()` instance method. This method will return the current status of the automaton, an instance
  of the `hoca.core.automata_framework.AutomatonStatus` class.
  
- `describe()` class method. This method will return a string describing the automata class.

We also have to implement the `__init__()` method without omitting to call `super().__init__()` to invoke
the corresponding function of the parent class. As we are interested in higher-order automata,
the `__init__()` method has the responsibility to initialize the state or "memory" of the automaton for
later use.

Let say we want to write an automata class that shuffles the content of a field containing an image, moving
the pixels along a specified distance and in a random direction. That may look similar to the [_Spread_ filter
of the GNU Image Manipulation Program](https://docs.gimp.org/2.10/en/gimp-filter-noise-spread.html).

The code below is an implementation of such an antomaton. It is commented to explain how it works, but you'll
find more explanations below it.

```python
# Import the needed modules.
import random

from hoca.core.automata_framework import Automaton, AutomatonStatus
from hoca.core.ImageField import ImageField
from hoca.core.utilities import AutomataUtilities


class SpreadingAutomaton(Automaton):
    # The amount class variable determines how far a pixel will be moved.
    amount = 5

    @classmethod
    def build_field_dict(cls, image_path):
        # Build a field dictionary:
        # - The source field is a read-only field built from the provided image.
        # - The result field is a blank write-only field the same size of the source field.
        source_field = ImageField.from_image(image_path, io_mode=ImageField.IOMode.IN, image_mode="RGB")
        return {'source': source_field,
                'result': ImageField.blank(source_field.size, io_mode=ImageField.IOMode.OUT, image_mode="RGB")}

    def __init__(self, automata_population):
        super().__init__()

        # Keep a shortcut to the fields, it improves readability
        # and may be efficient as it is accessed quite often.
        # Set a shortcut to the fields from the fields dictionary
        self.source_field = automata_population.field_dict['source']
        self.result_field = automata_population.field_dict['result']

        # Set an initial random position for the automaton
        self.x = random.randint(0, self.source_field.width - 1)
        self.y = random.randint(0, self.source_field.height - 1)

        # As the automaton will move the pixel (it's colour actually) we also need to keep track
        # we need a property to store the colour information while it's moved.
        # This property is initialized with the colour value of the pixel at its current position
        self.colour = self.source_field[self.x, self.y]

        # We also need to know how far the pixel has been moved up to now.
        self.distance = 0

        # Set the automaton life expectancy from the population size and the dimensions of the field.
        # In order to have a chance to move every pixels of the image we will choose this property of the
        # automaton such that the number of pixels to be processed by an automaton is equal to
        # the total number of pixels in the image divided by the number of automata.
        # Note that, as the process is stochastic, it doesn't ensure that all pixels will be moved,
        # it just allows it.
        self.pixel_count_before_death = \
            self.source_field.width * self.source_field.height // automata_population.population_size

        # Finally, set it alive.
        self.status = AutomatonStatus.ALIVE

    def run(self):
        # Check if the automaton with its pixel/color has moved enough
        if self.distance == self.amount:
            # ... the pixel has been moved enough
            # Set the color of the pixel at the current automaton position (on the result field)
            self.result_field[self.x, self.y] = self.colour

            # Decrease the number of pixels to be processed
            self.pixel_count_before_death -= 1
            # If the automaton has processed enough pixels, make it die.
            if self.pixel_count_before_death == 0:
                self.status = AutomatonStatus.DEAD
                # And end run
                return

            # The automaton is still alive and it has still some pixels to process...
            # Get the pixel color under the automaton (on the source field).
            self.colour = self.source_field[self.x, self.y]

            # Reset the distance traveled
            self.distance = 0

        # Move the automaton on one of the adjacent position:
        # Choose a direction randomly and update the automaton position.
        direction = random.randint(0, 7)
        self.x, self.y = AutomataUtilities.get_x_y(direction, self.x, self.y)
        # The direction may make the automaton pass a border of the field. So we need to wrap the coordinates
        # around the field (or the contrary?). i.e. If the direction makes the automaton pass the right border
        # of the field it will be moved to the left border and vice versa (the same for the top and bottom borders).
        self.x, self.y = AutomataUtilities.wrap_coordinates(self.x, self.y, *self.source_field.size)

        # Increase the count of the distance traveled so far
        self.distance += 1

    def get_status(self):
        # Just return a status
        return AutomatonStatus(self.status, self.x, self.y)

    @classmethod
    def describe(cls, short=True):
        if short:
            return f"{super().describe(short=short)}-{cls.amount}"
        else:
            return f"""{super().describe(short=short)}
    amount: {cls.amount}"""
```

The `build_field_dict()` method will prepare the field dictionary for the automata population. There are (as usual)
many ways to look at that. The most obvious is to have a dictionary with two fields: one field filled with the source image
and one initially empty field to be filled by the automata process.

The `__init()__` method initializes the state of the automaton. This state will contain the necessary properties
the automaton must "know" from one generation to the next. These are, for example, the position (x, y) of the
automaton on the fields or its status (is it living or dead?).  
In the automata class we are coding, we also need  to retain the colour of the pixel the automata is moving, 
and the distance it has traveled. Hence, the `colour` instance variable is initialized with the colour found
at the automaton initial position and the `distance` is initialized to 0 (has the automaton has not moved yet).  
Except if you always know in advance the number of generation the whole population of automata has to be run,
it is also useful to have some sort of counter to control the life expectancy of each automaton.
In our case, the `pixel_count_before_death` instance variable will be decreased each time the automaton has
completed a pixel move. The initial value of this variable will depend on the image size and the number of
automata in the population. Then, when the variable goes to zero, the automaton will die.

It is very important to call the `__init()__` method of the parent class (however, the location of the call
isn't necessarily at the beginning of the method). In the case of our `SpreadingAutomaton` class, the parent class
is the abstract `Automaton` which `__init()__` method sets the status property of the automaton to
`AutomatonStatus.ALIVE` in order to let it run on the first population generation.

The `run()` method will do the work of the automaton for one generation. It's obviously the most interesting
part of the automaton to write. In the case of the `SpreadingAutomaton` there are four things we need to handle:

- The writing of the pixel colour currently stored in the `colour` variable when the automaton has moved enough.

- The death of the automaton. It has to move a number of pixel colours equal to the value of `pixel_count_before_death`
  variable. After that, the automaton should die.
  
- The reading of a new pixel colour when the automaton has completed the handling the previous pixel colour.

- The movement of the automaton. It has to travel a number of pixels equal to the value of the `amount` class variable.

The writing of the `get_status()` method is straightforward, it just had to return the `status` variable (along with
the coordinates). But in some cases, the `run()` method don't or cannot compute the status, or it depends on an event
external to the automaton instance or not occurring while the `run()` method is executed. Then, the automaton status
should be computed in the `get_status()` method.

There is not much to say about the `describe()` method except it's a class method and it can't report about
the automaton instance. Note this may change in the future.

So we wrote the class, now we need to run it. We'll follow the same path as in the previous section using the
`CallbackPopulation` class to run a population of automata while having some report about what's going on.

```python
if __name__ == "__main__":
    from hoca.monitor.CallbackPopulation import CallbackPopulation, LogProgressCallback

    # Init the pseudo random generator to be able to replay the same population behaviour
    # This is optional
    random.seed('This is the seed')

    automata_class = SpreadingAutomaton

    # We can change the amount class property to spread the pixels farther.
    # SpreadingAutomaton.amount = 10

    # Build field
    field_dict = automata_class.build_field_dict("images/EdwardHopper_Nighthawks_1942.jpg")

    # Create the automata population
    automata_count = 1000
    automata_population = CallbackPopulation(field_dict, automata_count, automata_class)

    # Register a logging callback
    automata_population.register_callback(LogProgressCallback(automata_population))

    # Play the population
    automata_population.play(stop_after=1000000)

    # Display the result
    field_dict["result"].image.show()
```

Note that the `play()` method of the population is called with an arbitrary large number because the automata determine
by themselves (with the `pixel_count_before_death` variable) the number of generations needed to achieve their job.
So the `play()` method will return when all the automata have died even if it's before having reached the millionth
generation.

![Spread Nighthawks](https://github.com/g-art-dev/hoca/raw/main/images/SpreadingAutomaton_A1000_I1931_result-withstains.jpg)
> Hopper's Nighthawks after 1931 generations with 1000 SpreadAutomaton automata (with stains).  
> (_result field_)

You can see in the result of the execution of the automata code above. There are black stains on the spread
image. This is not necessarily desirable, and it comes from the randomness of the coverage of the fields by the
automata.
In order to avoid this phenomenon (or at least hide it), we can pre-fill the result field with the original image.
This is done with a rewritten `build_field_dict()` method.

```python
    @classmethod
    def build_field_dict(cls, image_path):
        # As the course of the automata is random (see the run() method), the source and/or result fields
        # will probably not be covered entirely and the result field will contain black/blank pixels. In order to
        # have a (more interesting?) result without those blank spots, one can pre-fill the result field with the
        # source image:
        # - The source field is a read-only field built from the provided image.
        # - The result field is a write-only field built from the provided image.
        return {'source': ImageField.from_image(image_path, io_mode=ImageField.IOMode.IN, image_mode="RGB"),
                'result': ImageField.from_image(image_path, io_mode=ImageField.IOMode.OUT, image_mode="RGB")}
```

![Spread Nighthawks](https://github.com/g-art-dev/hoca/raw/main/images/SpreadingAutomaton_A1000_I1931_result-nostain.jpg)
> Hopper's Nighthawks after 1931 generations with 1000 SpreadAutomaton automata (without stain).  
> (_result field_)

A similar result could have been achieved by using a single input-output field. The automata would have read and
write the colours on the same field, swapping the pixels at the beginning and the end of the move, or taking the colour
found at the end of the move for the next move.

The code of the `run()` method is quite demonstrative and may be easily enhanced if the user is in need of performance.
At the moment, it takes a number of generations equal to the `amount` class variable for an automaton to move the colour.
But this could be done in a single generation:

```python
    # Compute the relative destination position.
    dx = random.randint(-self.amount, self.amount)
    dy = random.randint(-self.amount, self.amount)
    # As |dx| may be greater than 1 (the same for |dy|), the automaton will "jump" from
    # its current position to the next.

    # Compute the destination coordinates wrapping them if they're out of the field.
    self.x, self.y = AutomataUtilities.wrap_coordinates(self.x + dx, self.y + dy, *self.source_field.size)

    # Finally, update the distance travelled.
    self.distance = self.amount
```

As a final thought about this automata class, using a cellular automaton to do this kind of operation on an image isn't 
probably the most efficient way to get a result. However, this approach allows thinking locally (at the pixel level)
instead of globally (at the image level) and may lead to simpler investigation of an idea.

## Limitations

At the moment, automata are not aware of each other. This means you can't use the `hoca` library
to implement classic automata, the Conway's game of life for instance. You can do it actually,
but it will be in O(N²) as each automaton will have to look at all other automata in the population
to know if some are its neighbours.

## Advertising hoca

It would be greatly appreciated by the authors if the images and other productions made with the `hoca` library
were accompanied by a citation naming it; something like:  

> This <work> was produced with the `hoca` library (https://pypi.org/project/hoca/).

You might also send us a little mail about what you're doing with `hoca`.

## Licencing & contribution

`hoca` is a free software library written at [Villa Arson](https://www.villa-arson.fr/) and
[I3S](https://www.i3s.unice.fr/) and released on GitHub under the LGPLv3 license.
You should have received a copy of the GNU Lesser General Public License
along with `hoca`. If not, see http://www.gnu.org/licenses/.

The library is copyrighted by its contributors (see source file headers).

There is a lot of room for improvements, everyone is welcome to contribute if you find any bug or have ideas
for new features!

## Bibliography

[1] Formenti E., Paquelin JL. (2021) _High Order Cellular Automata for Edge Detection: A Preliminary Study_.
_In_: Cellular Automata. ACRI 2020. Lecture Notes in Computer Science, vol 12599. Springer,
Cham. https://doi.org/10.1007/978-3-030-69480-7_9
