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

from .automata_framework import Population, AutomatonStatus

import random
from enum import Enum


class BasicPopulation(Population):
    """This class provides an execution environment for the automata population.

    Each time the run() method is invoked, each automaton is ran once. At the end of the run
    the population may have increased or decreased.

    Status: as each automaton has its own status, population as a whole has a status.
    These are the available status values:
    EMPTY: the population has decreased to 0 before reaching the final condition.
    COMPLETED: the population has reached the expected final condition.
    RUNNABLE: the run() method should be called in order to reach the final condition.

    The final condition depends on the automata and the data they have to process. It is expressed
    as a number of generations (or a number of runs).
    """

    class Status(Enum):
        RUNNABLE = 0
        COMPLETED = 1
        EMPTY = 2

    def __init__(self, field_dict, population_size, automata_class,
                 auto_respawn=False, generation_to_complete=None, shuffle=False):
        """The initializer method prepares the automata population, i.e. it instantiates the
        automata. It must receive some mandatory values:
        - field_dict: the fields to process,
        - population_size: the number of automata to instantiate,
        - automata_class: the class of the automata.

        The class behaviour may be controlled by passing some keyword parameters:
        - auto_respawn (False by default): If TRUE, at each generation, all automata with a DEAD
          status are reinstantiated.
        - generation_to_complete (None by default): Sets the number of execution/run/generation
          a population must achieve before it is completed (i.e. self.status == Status.COMPLETED).
          If generation_to_complete is None, the population may be ran an unlimited number of times.
        - shuffle (False by default): If TRUE, the automata are shuffled after each generation. This
          prevents a deterministic order of execution of the automata.

        :param field_dict: dict of fields
        :param population_size: int
        :param automata_class: Automaton
        :param auto_respawn: bool
        :param generation_to_complete: int or None
        :param shuffle: bool
        """
        assert generation_to_complete is None or generation_to_complete >= 0,\
            f"generation_to_complete should be None or greater than or equal to 0 ({generation_to_complete})"

        super().__init__()

        # Store the parameters
        self.field_dict = field_dict
        self.population_size = population_size
        self.automata_class = automata_class

        self.auto_respawn = auto_respawn
        self.generation_to_complete = generation_to_complete
        self.shuffle = shuffle

        # create the initial automata population
        self.automata_population = list(map(lambda _: automata_class(self), range(population_size)))

        if self.population_size == 0:
            self.status = BasicPopulation.Status.EMPTY
        else:
            self.status = BasicPopulation.Status.RUNNABLE

    def run(self):
        """run() method \"processes\" one generation. If the population is status is RUNNABLE,
        for each automaton in the population:
        - If the automaton status is ALIVE, it runs the automaton and add it to the next
          generation generation to be ran.
        - If the automaton status is DEAD, it won't be added to the next generation population
          except if the auto_respawn property is True. In this case, it will be treated as if
          its status was RESPAWN.
        - If the automaton status is RESPAWN, a freshly instantiated automaton is added to the
          generation population.

        If the shuffle property is set to True, the next generation population is then shuffled.

        :return: the population status
        """
        if self.status != BasicPopulation.Status.RUNNABLE:
            return self.status

        super().run()

        next_automata_population = []

        for automaton in self.automata_population:
            # Process the automaton according to its status
            # We can't suppose that all the automata are ALIVE even at the
            # first generation, their statuses may have been changed by an
            # external condition
            status = automaton.get_status()
            if status.s == AutomatonStatus.ALIVE:
                # automaton is alive, run it
                automaton.run()
                next_automata_population.append(automaton)
            elif status.s == AutomatonStatus.RESPAWN:
                next_automata_population.append(self.automata_class(self))
            elif status.s == AutomatonStatus.DEAD:
                if self.auto_respawn:
                    # replace the dead automaton by a new one
                    next_automata_population.append(self.automata_class(self))

        # shuffle the population execution order before the next run
        if self.shuffle:
            random.shuffle(next_automata_population)

        # update the population for the next generation
        self.automata_population = next_automata_population
        self.population_size = len(self.automata_population)

        # All the automata have died
        if self.population_size == 0:
            self.status = BasicPopulation.Status.EMPTY
            return self.status

        # If the generation number has reached the number of generation to complete the job...
        if self.generation_to_complete is not None and self.generation >= self.generation_to_complete:
            self.status = BasicPopulation.Status.COMPLETED
            return self.status

        return self.status

    def play(self, stop_after=1):
        """The play() method runs the population multiple times. The maximum number
        of population runs depends on the value of the stop_after keyword parameter.
        The actual number of generation ran may be less than expected as the population
        status may have changed to EMPTY or COMPLETED.

        As the default value of stop_after is 1, calling play() without parameter does
        the same as calling run().

        :type stop_after: int
        """
        for _ in range(stop_after):
            if self.run() != self.Status.RUNNABLE:
                break

        return self.status

    def describe(self, short=True):
        """The describe() method outputs a string describing the population.
        If the short keyword parameter is True the output will contains one line,
        otherwise it will contain multiple lines.

        :param short: bool
        :return: str
        """

        if short:
            return f"{self.automata_class.describe(short=short)}_" \
                   f"g{self.generation}_" \
                   f"s{self.population_size}(actual {len(self.automata_population)})"
        else:
            return f"""Population: {self.__class__.__name__}
    generation: {self.generation}
    size: {self.population_size}
    status: {self.status}
    auto_respawn: {self.auto_respawn}
    generation_to_complete: {self.generation_to_complete}
    shuffle: {self.shuffle}
    automata: {self.automata_class.describe(short=False)}"""

