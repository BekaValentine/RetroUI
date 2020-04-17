import math
import PIL.Image as PIL
from retroui.terminal.color import *
from retroui.terminal.size import *
from retroui.terminal.tixel import *


class Image(object):
    """
    A wrapper around PIL's images.

    Slots:

        `file_path`
            The file path used to load this image.

        `_PIL_image`
            The PIL image this wraps.

        `size`
            The dimensions of the image.

        `_color_cache`
            A cache of the color rendering.
    """

    @staticmethod
    def pixel_to_bit(px):
        return int(px / 255)

    @staticmethod
    def pixels_to_byte(img, x, y):
        return Image.pixel_to_bit(img.getpixel((x, y))) << 0 | \
            Image.pixel_to_bit(img.getpixel((x, y + 1))) << 1 | \
            Image.pixel_to_bit(img.getpixel((x, y + 2))) << 2 | \
            Image.pixel_to_bit(img.getpixel((x + 1, y))) << 3 | \
            Image.pixel_to_bit(img.getpixel((x + 1, y + 1))) << 4 | \
            Image.pixel_to_bit(img.getpixel((x + 1, y + 2))) << 5 | \
            Image.pixel_to_bit(img.getpixel((x, y + 3))) << 6 | \
            Image.pixel_to_bit(img.getpixel((x + 1, y + 3))) << 7

    @staticmethod
    def byte_to_braille(byt):
        return chr(0x2800 + byt)

    @staticmethod
    def image_to_braille(image):
        # convert the size up to compensate for brail chars being 1/2 wide and
        # 1/4 tall
        new_width = 1 * image.width
        new_height = 1 * image.height

        # convert the size to a multiple of two and four
        new_width = 2 * math.ceil(new_width / 2)
        new_height = 4 * math.ceil(new_height / 4)

        image = image.resize((new_width, new_height))

        dithered = image.convert('1')

        lines = []

        for y in range(math.ceil(dithered.height / 4)):
            line = []
            for x in range(math.ceil(dithered.width / 2)):
                line.append(Tixel(Image.byte_to_braille(
                    Image.pixels_to_byte(dithered, 2 * x, 4 * y)), Color.White, Color.Black))
            lines.append(line)

        return lines

    @staticmethod
    def image_to_braille_high_contrast(image):
        # convert the size up to compensate for brail chars being 1/2 wide and
        # 1/4 tall
        new_width = 1 * image.width
        new_height = 1 * image.height

        # convert the size to a multiple of two and four
        new_width = 2 * math.ceil(new_width / 2)
        new_height = 4 * math.ceil(new_height / 4)

        image = image.resize((new_width, new_height))

        quantized = image.quantize(colors=127)
        dithered = quantized.convert('1')

        lines = []

        for y in range(math.ceil(dithered.height / 4)):
            line = []
            for x in range(math.ceil(dithered.width / 2)):
                line.append(Tixel(Image.byte_to_braille(
                    Image.pixels_to_byte(dithered, 2 * x, 4 * y)), Color.White, Color.Black))
            lines.append(line)

        return lines

    @staticmethod
    def pixels_to_color_block_element(image, xcoord, ycoord):
        top = image.getpixel((xcoord, ycoord))
        bottom = image.getpixel((xcoord, ycoord + 1))
        return Tixel('▀', Color(*top, 255), Color(*bottom, 255))

    @staticmethod
    def image_to_color_block_elements(image):
        # convert height to a multiple of 2
        new_height = 2 * math.ceil(image.height / 2)
        image = image.resize((image.width, new_height))

        # convert to RGB
        image = image.convert('RGB')

        lines = []
        for y in range(math.ceil(image.height / 2)):
            ycoord = 2 * y
            line = []
            for xcoord in range(image.width):
                line.append(Image.pixels_to_color_block_element(
                    image, xcoord, ycoord))
            lines.append(line)

        return lines

    __slots__ = ['file_path', '_PIL_image', 'size', '_color_cache',
                 '_braille_cache', '_braille_high_contrast_cache']

    def __init__(self, file_path, _PIL_source=None):
        self.file_path = file_path

        if isinstance(_PIL_source, PIL.Image):
            self._PIL_image = _PIL_source
        elif _PIL_source is None:
            self._PIL_image = PIL.open(self.file_path)

        self.size = Size(self._PIL_image.width, self._PIL_image.height)

        self._color_cache = None
        self._braille_cache = None
        self._braille_high_contrast_cache = None

    def image_by_resizing(self, new_size):
        new_width = max(1, int(new_size.width))
        new_height = max(1, int(new_size.height))
        return Image(self.file_path, _PIL_source=self._PIL_image.resize((new_width, new_height)))

    def image_by_scaling(self, frac):
        return self.image_by_resizing(Size(frac * self.size.width, frac * self.size.height))

    def color_at_point(self, pt):
        col = self._PIL_image.getpixel((pt.x, pt.y))
        return Color(*col)

    def copy(self):
        return Image(self.file_path, _PIL_source=self._PIL_image.copy())

    def braille_representation(self):
        if self._braille_cache is None:
            self._braille_cache = Image.image_to_braille(self._PIL_image)
        return self._braille_cache

    def braille_representation_high_contrast(self):
        if self._braille_high_contrast_cache is None:
            self._braille_high_contrast_cache = Image.image_to_braille_high_contrast(
                self._PIL_image)
        return self._braille_high_contrast_cache

    def color_representation(self):
        if self._color_cache is None:
            self._color_cache = Image.image_to_color_block_elements(
                self._PIL_image)
        return self._color_cache
