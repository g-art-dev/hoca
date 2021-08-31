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

from hoca.core.automata_framework import Field
from PIL import Image
import numpy


class ImageField(Field):
    """The ImageField class is an implementation of the abstract Field class. It allows
    the creation of fields based on the content of an image or the interpretation of a field
    as an image.

    ImageField have 2D discreet coordinates (they are pixel coordinates after all) which give
    access to a 3rd dimension (the depth of the field) of a triplet of RGB values or a quadruplet
    of RGBA values. These color component values are in the [0.0, 1.0] interval.

    WARNING: even if ImageField instances have __getitem__() and __setitem__()
    that return numpy arrays, you can't write:
        my_image_field = my_image_field / 2
    You should write instead:
        my_image_field[:, :, :] = my_image_field[:, :, :] / 2
    or
       my_image_field.data = my_image_field.data / 2
    That's because ImageField inherits of Field and numpy is just a client class.
    """

    @classmethod
    def from_image(cls, image_path, image_mode=None, **kwargs):
        """The from_image() class method returns an instance of ImageField which content
        corresponds to an image content.

        :param image_path: A filename (string), pathlib.Path object or a file object.
        The file object must implement ``file.read``, ``file.seek``, and ``file.tell`` methods,
        and be opened in binary mode.
        :param image_mode: str PIL.Image mode
        See: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
        :param kwargs: these are passed to the class constructor
        :return: ImageField instance
        """
        image = Image.open(image_path)

        if image_mode is not None:
            image = image.convert(mode=image_mode)

        return cls(image, **kwargs)

    @classmethod
    def blank(cls, size, image_mode=None, **kwargs):
        """The blank() class method returns an instance of ImageField which content
        is set to 0.0.

        :param size: a pair, containing (width, height) of the field.
        :param image_mode: str PIL.Image mode
        See: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
        :param kwargs: these are passed to the class constructor
        :return: ImageField instance filled with zeros
        """
        image = Image.new(image_mode, size)

        return cls(image, **kwargs)

    def __init__(self, image, **kwargs):
        """The initializer method fills the field instance with the pixel data of the PIL
        Image passed in the image parameter.

        Important notice:
        PIL images have a mode (see: https://pillow.readthedocs.io/en/stable/handbook/concepts.html)
        which specifies the size of the data hold on each pixel. This class doesn't handle all the PIL
        modes. Supported modes are:

        - L (8-bit pixels, black and white)

        - RGB (3x8-bit pixels, true color)

        - RGBA (4x8-bit pixels, true color with transparency mask)

        - CMYK (4x8-bit pixels, color separation)

        - YCbCr (3x8-bit pixels, color video format)

        - HSV (3x8-bit pixels, Hue, Saturation, Value color space)

        :param image: PIL.Image
        """
        assert image.mode in ("L", "RGB", "RGBA", "CMYK", "YCbCr", "HSV"), "Unsupported PIL image mode"

        super().__init__(**kwargs)

        # Keep track of the data in its source format
        self._image = image

        # Convert the image data as a numpy array
        self._data = numpy.asarray(image)

        # It can be a 2D array when the image as only one band (as in a grayscale image)
        # add a 3rd dimension to have an homogenous 3D representation
        if len(self._data.shape) == 2:
            self._data = self._data[..., numpy.newaxis]
            self._data_2d = True
        else:
            self._data_2d = False

            # The PIL Image and the numpy array have their coordinates swapped.
        # The reason is PIL.Image.size: (width, height) while numpy.ndarray.shape is (rows, columns).
        # So we need to transpose() transpose the array.
        self._data = self._data.transpose(1, 0, 2)

        # Add finally, convert the image data as values in [0, 1]
        # We can divide the numpy array by 255 because all the (supported) PIL images modes are
        # byte wise.
        self._data = self._data / 255

        # The _data_written private property tells if the current content of _image
        # ISN'T the same as the _data property that contains the numpy representation.
        self._data_written = False  # for now, they are the same

        # If the field is read only, configure the internal numpy data representation accordingly.
        if self.io_mode == Field.IOMode.IN:
            # The data should not be changed
            self._data.setflags(write=False)

    @property
    def image(self):
        """The image() method returns a PIL Image representation of the field data.

        :return: PIL.Image
        """
        if self._data_written:
            # convert data back to the image
            # rebuild the image from the numpy data
            image_data = (self._data.transpose(1, 0, 2) * 255).astype(numpy.uint8)

            if self._data_2d:
                # Remove the 3rd dimension
                image_data = image_data[:, :, 0]

            self._image = Image.fromarray(image_data)

        return self._image

    @property
    def size(self):
        """The size() method returns the 2D size of the ImageField.

        :return: a pair, containing (width, height) of the field.
        """
        return self._image.size

    @property
    def width(self):
        """The field width

        :return: int
        """
        return self._image.width

    @property
    def height(self):
        """The field height

        :return: int
        """
        return self._image.height

    @property
    def depth(self):
        """The field depth

        :return: int
        """
        return len(self._image.getbands())

    @property
    def data(self):
        """The numpy data of the field"""
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def __getitem__(self, idx):
        """The __getitem__() special method defines the interface to read the data
        in the field.

        Index 0 is the abscissa. Its value is constrained by the width of the field.
        Index 1 is the ordinate. Its value is constrained by the height of the field.
        Index 2 is the color component selector. Its value is constrained by the depth of the field.

        See: https://docs.python.org/3/reference/datamodel.html#object.__getitem__

        :param idx: slice
        :return: a value
        """
        return self._data[idx]

    def __setitem__(self, idx, value):
        """The __setitem__() special method defines the interface to write the data
        in a field.

        Index 0 is the abscissa. Its value is constrained by the width of the field.
        Index 1 is the ordinate. Its value is constrained by the height of the field.
        Index 2 is the color component selector. Its value is constrained by the depth of the field.

        See: https://docs.python.org/3/reference/datamodel.html#object.__setitem__

        :param idx: slice
        :param value:
        :return: None
        """
        self._data[idx] = value
        self._data_written = True

    def is_in(self, coordinates):
        """Tests if some coordinates are within the field.
        If a coordinate value is None, it will be be ignored. So calling my_field.is_in((3, None, 2))
        will only check the first and the third coordinates against the field dimensions.

        Note: Even if the ImageFields are implemented with numpy arrays accepting negative indices,
        the is_in() method will return False for any negative coordinates.

        :param coordinates: tuple
        """
        for length, coordinate in zip(self._data.shape, coordinates):
            if coordinate is not None and (coordinate < 0 or coordinate >= length):
                return False
        return True

    def __str__(self):
        return f"""Field: {self.__class__.__name__}
    width: {self.width}
    height: {self.height}
    mode: {self._image.mode}"""


if __name__ == "__main__":
    # Create a blank ImageField of 10 by 10 cells
    # image_mode="RGBA" makes it correspond to an all black transparent image of 10x10 pixels.
    # And make the field readable and writable.
    image_field = ImageField.blank((10, 10), image_mode="RGBA", io_mode=ImageField.IOMode.INOUT)

    # Put a vector of 1s in the middle of the field
    # It will correspond to a solid white pixel in the image
    image_field[image_field.width // 2, image_field.height // 2] = 1

    # Put another vector at a cell in the field
    # It will correspond to a solid red pixel in the image
    image_field[image_field.width // 2, image_field.height // 4] = (1, 0, 0, 1)

    # Set the 4th component of a cell in the field to 1
    # It will make solid (instead of transparent) the corresponding point in the image
    # (this will be a black dot as the image background is black)
    image_field[image_field.width // 4, image_field.height // 2, 3] = 1

    # Get the field back as an image and display it
    image_field.image.show()

    # Create a blank ImageField of 10 by 10 cells
    # image_mode="L" makes it correspond to an all black image of 10x10 pixels.
    # And make the field readable and writable.
    image_field = ImageField.blank((10, 10), image_mode="L", io_mode=ImageField.IOMode.INOUT)

    # Put a value of 1s in the middle of the field
    # It will correspond to a white pixel in the image
    image_field[image_field.width // 2, image_field.height // 2] = 1

    # Put another value at a cell in the field
    # It will correspond to a dark grey pixel in the image
    image_field[image_field.width // 2, image_field.height // 4] = 0.33

    # Draw a light grey pixel
    # One can specify the 3rd dimension index even if it's always 0 on a grayscale ImageField
    image_field[image_field.width // 4, image_field.height // 2, 0] = 0.66

    # Get the field back as an image and display it
    image_field.image.show()
