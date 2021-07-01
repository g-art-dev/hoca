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

from PIL import Image

size = (256, 256)
basename = "test_image"


def make_image(basename, size, step):
    image = Image.new("RGBA", size)
    image_data = image.load()
    for x in range(size[0]):
        for y in range(size[1]):
            r = (x // step) * step
            g = (y // step) * step
            b = 255 - r
            a = 255 - g
            image_data[x, y] = (r, g, b, a)

    image.save(f"{basename}_step={step}.png")


for step in (1, 16, 64):
    make_image(basename, size, step)
