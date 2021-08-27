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

# Import the needed modules.
import random

from hoca.core.automata_framework import Automaton, AutomatonStatus
from hoca.core.ImageField import ImageField
from hoca.core.utilities import AutomataUtilities


class SpreadingAutomaton(Automaton):
    """
    The SpreadingAutomaton is a toy automata class. It spreads the pixels af an image
    in some way similar to the Gimp's Spread filter.

    See: https://docs.gimp.org/2.10/en/gimp-filter-noise-spread.html
    """

    """
    The amount class variable determines how far a pixel will be moved.
    """
    amount = 5

    @classmethod
    def build_field_dict(cls, image_path):
        """The build_field_dict() class method builds a field distionary to be used with a population of
        SpreadingAutomaton.

        :parameter image_path: PIL Image
        :return: a field dictionary"""
        # Build a field dictionary:
        # - The source field is a read-only field built from the provided image.
        # - The result field is a blank write-only field the same size of the source field.
        # source_field = ImageField.from_image(image_path, io_mode=ImageField.IOMode.IN, image_mode="RGB")
        # return {'source': source_field,
        #         'result': ImageField.blank(source_field.size, io_mode=ImageField.IOMode.OUT, image_mode="RGB")}

        # As the course of the automata is random (see the run() method below), the source and/or result fields
        # will probably not be covered entirely and the result field will contain black/blank pixels. In order to
        # have a (more interesting?) result without those blank spots, one can pre-fill the result field with the
        # source image:
        # - The source field is a read-only field built from the provided image.
        # - The result field is a write-only field built from the provided image.
        return {'source': ImageField.from_image(image_path, io_mode=ImageField.IOMode.IN, image_mode="RGB"),
                'result': ImageField.from_image(image_path, io_mode=ImageField.IOMode.OUT, image_mode="RGB")}

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


if __name__ == "__main__":
    from hoca.monitor.CallbackPopulation import CallbackPopulation, LogProgressCallback

    # Init the pseudo random generator to be able to replay the same population behaviour
    # This is optional
    random.seed('This is the seed')

    automata_class = SpreadingAutomaton

    # We can change the amount class property to spread the pixels farther.
    # SpreadingAutomaton.amount = 10

    image_path = '../../images/EdwardHopper_Nighthawks_1942.jpg'

    # Build field
    field_dict = automata_class.build_field_dict(image_path)

    # Create the automata population
    automata_count = 1000
    automata_population = CallbackPopulation(field_dict, automata_count, automata_class)

    # Register a logging callback
    automata_population.register_callback(LogProgressCallback(automata_population))

    # Play the population
    automata_population.play(stop_after=1000000)

    # Display the result
    field_dict["result"].image.show()

    # Save the result
    # field_dict["result"].image.save("SpreadingAutomaton_A1000_I1931_result-nostain.jpg")
