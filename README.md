# hoca: an Higher-Order Cellular Automata Python Library

## Overview

## Installation
The latest version of `hoca` is installed via a standard pip command:

```shell
pip install hoca
```

## Advertising hoca

It would be greatly appreciated by the authors if the images and other productions made with the `hoca` library
were accompanied by a citation naming it; something like:  
"This <work> was produced with the `hoca` library (https://pypi.org/project/hoca/)".

## Data Structures

### Population classes

#### `hoca.core.automata_framework.Population`
The Population class is abstract. It's the root of the population classes hierarchy.

#### `hoca.core.BasicPopulation`
BasicPopulation class inherits of the Population class and implements the base functionalities
of a population:

- It instanciates the automata,
- it controls if the died automata are respawned for the next generation,
- it may stop the execution of the automata population after a predefined number
  of generations,
- it allows to shuffle the automata's order of execution.

#### `hoca.monitor.CallbackPopulation`
CallbackPopulation class inherits of the BasicPopulation class. It provides a way to
monitor the automata population throughout the successive generations.

CallbackPopulation module contains both the CallbackPopulation population class and 
the Callback class hierachy.

### Fields

Fields are data structures which hold the source data process by an automata population
and the result data produced by them. Fields can also be both source and result at the same time. This way
the automata can modify the field *in place*.  
Field data structure features are defined in the `hoca.core.automata_framework.Field` class (which is abstract).
The implementation is in `hoca.core.ImageField`.  
In order to do their work, one must provide appropriate fields to the automata
population. The best and simplest way to prepare the fields, is to call the
build_field_dict() class method of the automata class.

The build_field_dict() returns a dictionary with one entry per field.

Fields have an IOMode which defines if they are:  
    - readable: Field.IOMode.IN 
    - writable: Field.IOMode.OUT
    - readable and writable: Field.IOMode.INOUT

## Contribute !
`hoca` is an open-source library written at [Villa Arson](https://www.villa-arson.fr/) and
[I3S](https://www.i3s.unice.fr/) and released on GitHub under the LGPLv3 license.
The library is copyrighted by its contributors (see source file headers).

There is a lot of room for improvements, everyone is welcome to contribute if you find any bug or have idea
for new features!
