# hoca: an Higher-Order Cellular Automata Python Library

## Overview

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
this way the automata can modify the field *in place*.  

For this purpose fields have an io_mode property that defines if they are:  
- readable: io_mode == Field.IOMode.IN
- writable: io_mode == Field.IOMode.OUT
- readable and writable: io_mode == Field.IOMode.INOUT

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

There are two methods:
- `run()` which runs all the automata once (i.e. one generation),
- `play()` which runs all the automata for multiple generations.

The first is the most complex of the two as `play()` simply calls `run()` repeatedly.

##### `hoca.core.BasicPopulation`

BasicPopulation class inherits of the Population class and implements the base functionalities
of a population:

- It instantiates the automata,
- it controls if the died automata are respawned for the next generation,
- it may stop the execution of the automata population after a predefined number
  of generations,
- it allows to shuffle the automata's order of execution.

##### `hoca.monitor.CallbackPopulation`
CallbackPopulation class inherits of the BasicPopulation class. It provides a way to
monitor the automata population throughout the successive generations.

CallbackPopulation module contains both the CallbackPopulation population class and 
the Callback class hierachy.

## Limitations

At the moment, automata are not aware of each other. This means you can't use the `hoca` library
to implement the Conway's game of life. You can do it actually, but it will be in O(N²) as each automaton
will have to look at all other automata in the population to know if some are its neighbours.

## Advertising hoca

It would be greatly appreciated by the authors if the images and other productions made with the `hoca` library
were accompanied by a citation naming it; something like:  

> This <work> was produced with the `hoca` library (https://pypi.org/project/hoca/).

You could also send us a mail about what you're doing with `hoca`.

## Contribute !
`hoca` is an open-source library written at [Villa Arson](https://www.villa-arson.fr/) and
[I3S](https://www.i3s.unice.fr/) and released on GitHub under the LGPLv3 license.
The library is copyrighted by its contributors (see source file headers).

There is a lot of room for improvements, everyone is welcome to contribute if you find any bug or have idea
for new features!
