# Copyright (C) 2021 Jean-Louis Paquelin <jean-louis.paquelin@villa-arson.fr>
#
# This file is part of the hoca (Higher-Order Cellular Automata) library.
#
# hoca is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hoca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with hoca.  If not, see <http://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
from enum import Enum


class Field(ABC):
    """Field is an abstract class that defines the common basic features of the data structure
    on which the automata populations operate.

    The actual implementations of the Field class are constrained by this class. They must offer
    at least:
    - functions to read and write the data in the field,
    - a boolean function to say if some coordinates are in the field or not, this is useful if the
    field is finite.
    """

    class IOMode(Enum):
        """IOMode class is used to specify if the field is readable (IN), writable (OUT) or
        both (INOUT).
        Note this is not enforced however.
        """

        IN = 0
        OUT = 1
        INOUT = 2

    def __init__(self, io_mode=IOMode.IN):
        """The Field class initializer takes one keyword parameter. It is used to specify
        the accessibility of the data in the field structure.

        :param io_mode: IOMode enum (IN by default)
        """
        self.io_mode = io_mode

    @abstractmethod
    def __getitem__(self, idx):
        """The __getitem__() special abstract method defines the interface to read the data
        in a field.

        See: https://docs.python.org/3/reference/datamodel.html#object.__getitem__

        :param idx: slice
        :return: a value
        """
        pass

    @abstractmethod
    def __setitem__(self, idx, value):
        """The __setitem__() special abstract method defines the interface to write the data
        in a field.

        See: https://docs.python.org/3/reference/datamodel.html#object.__setitem__

        :param idx: slice
        :param value:
        :return: None
        """
        pass

    @abstractmethod
    def is_in(self, coordinates):
        """Returns
        - True if the coordinates points in the field,
        - and False they're outside the field.

        :param coordinates: list or tuple of ints
        :return: bool
        """
        pass

    # TODO: add a describe method


class Automaton(ABC):
    """Automaton abstract class defines the common features of the automata; mainly the job
    done by an automaton during one generation.
    """

    @classmethod
    @abstractmethod
    def build_field_dict(cls, *args, **kwargs):
        """The build_field_dict() abstract class method is a convenience method used to
        build the appropriate field dictionary to be used by a population of automata as they
        probably have to share the same field or fields.

        A Python dictionary is used here in order to allow the manipulation of multiple fields
        by the automata population and to facilitate human interpretation of the data structure.
        """
        return {}

    # TODO: add a class method providing the optimal number of automata for the current Field and set of parameters
    # TODO: add a class method providing the optimal number of generation for the current Field, set of parameters and number of automata

    def __init__(self):
        """The initializer method sets the automaton status to AutomatonStatus.ALIVE.
        The status should be updated at the end of each generation.
        """
        # Even if the class is abstract,
        # it provides the basic initialization
        self.status = AutomatonStatus.ALIVE

    @abstractmethod
    def run(self):
        """The run() abstract method has to be implemented in Automaton subclasses in order the
        define what an automaton has to do on each generation."""
        pass

    @abstractmethod
    def get_status(self):
        """The get_status() abstract method subclasses implementation will return the status of an
        automaton.
        :return: AutomatonStatus
        """
        pass

    @classmethod
    def describe(cls, short=True):
        """The describe() method is a convenience method used to get some textual information
        about an automata class.
        This method takes an optional boolean keyword parameter named short to specify if the
        reply has to be short or not.

        :type short: bool
        :return: str
        """
        # TODO: this is a class method, should it be an instance method instead?
        #  Or do we need a separate method to report the current state of the automaton?
        return cls.__name__


class AutomatonStatus:
    """The AutomatonStatus class is used to hold the status data of an automaton.

    The class defines 3 states:
    - DEAD: the automaton is dead it will not be run on the next generation.
    - ALIVE: the automaton is dead it will not be run on the next generation.
    - RESPAWN: the automaton is dead but should or may be resurrected on the
      next generation. Note that the exact semantics of the RESPAWN status is left to
      the appreciation of the implementer of the population class.
    """

    DEAD = 0
    ALIVE = 1
    RESPAWN = 2

    def __init__(self, s, x, y):
        """The initializer method sets the status and the coordinates kept in the AutomatonStatus
        instance properties.
        """
        assert s in (AutomatonStatus.DEAD, AutomatonStatus.ALIVE, AutomatonStatus.RESPAWN)

        self.s = s
        self.x = x
        self.y = y
        # TODO: this is limited to 2D coordinates, this should be generalized to nD.


class Population(ABC):
    """The Population abstract class defines the basic features of a population of automata,
    i.e. running each automaton code.
    """

    def __init__(self):
        """The initializer method sets the generation number property to 0 (as no
        automaton has been ran yet).
        """

        self.generation = 0

    @abstractmethod
    def run(self):
        """The run() abstract method has to be implemented in order to run (at least) all the
        automata for one generation.
        The method increases the generation number by 1.
        """
        self.generation += 1

    @abstractmethod
    def play(self):
        """The play() abstract method has to be implemented in order to run all the
        automata for a number of generation, it should probably be done by calling the run()
        method multiple times.

        The actual number of generation ran by the play() method is up to the implementer.
        """
        pass

    @abstractmethod
    def describe(self, short=True):
        """The describe() method is a convenience method used to get some textual information
        about a population (e.g. the number of automata which are ALIVE or the generation).
        This method takes an optional boolean keyword parameter named short to specify if the
        reply has to be short or not.

        :type short: bool
        :return: str
        """
        return self.__class__.__name__
