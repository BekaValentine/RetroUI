from typing import List, Optional, Tuple, Union

import math
import PIL.Image as PIL
from retroui.terminal.minmax import minmax
from retroui.terminal.color import *
from retroui.terminal.point import Point
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

    __slots__ = ['file_path', '_PIL_image', 'size', '_color_cache',
                 '_braille_cache', '_braille_high_contrast_cache']

    def __init__(self, file_path, _PIL_source=None):
        # type: (str, Optional[PIL.Image]) -> None
        self.file_path = file_path  # type: str

        if isinstance(_PIL_source, PIL.Image):
            self._PIL_image = _PIL_source  # type: PIL.Image
        elif _PIL_source is None:
            self._PIL_image = PIL.open(self.file_path)

        self.size = Size(self._PIL_image.width,
                         self._PIL_image.height)  # type: Size

        self._color_cache = None  # type: Optional[List[List[Tixel]]]
        self._braille_cache = None  # type: Optional[List[List[Tixel]]]
        self._braille_high_contrast_cache = None \
            # type: Optional[List[List[Tixel]]]

    def image_by_resizing(self, new_size):
        # type: (Size) -> Image
        new_width = max(1, int(new_size.width))  # type: int
        new_height = max(1, int(new_size.height))  # type: int
        return Image(self.file_path, _PIL_source=self._PIL_image.resize((new_width, new_height)))

    def image_by_scaling(self, frac):
        # type: (Union[int,float]) -> Image
        return self.image_by_resizing(Size(int(frac * self.size.width), int(frac * self.size.height)))

    def color_at_point(self, pt):
        # type: (Point) -> Color
        col = self._PIL_image.getpixel((pt.x, pt.y)) \
            # type: Tuple[int, int, int]
        return Color(col[0], col[1], col[2], 255)

    def copy(self):
        # type: ()-> Image
        return Image(self.file_path, _PIL_source=self._PIL_image.copy())

    def braille_representation(self):
        # type: () -> List[List[Tixel]]
        if self._braille_cache is None:
            self._braille_cache = image_to_braille(self._PIL_image)
        return self._braille_cache

    def braille_representation_high_contrast(self):
        # type: () -> List[List[Tixel]]
        if self._braille_high_contrast_cache is None:
            self._braille_high_contrast_cache = image_to_braille_high_contrast(
                self._PIL_image)
        return self._braille_high_contrast_cache

    def color_representation(self):
        # type: () -> List[List[Tixel]]
        if self._color_cache is None:
            self._color_cache = image_to_color_block_elements(
                self._PIL_image)
        return self._color_cache


def pixel_to_bit(px):
    # type: (int) -> int
    px = minmax(px, 0, 255)
    return int(px / 255)


def pixels_to_byte(img, x, y):
    # type: (PIL.Image, int, int) -> int
    x = max(0, x)
    y = max(0, y)
    return pixel_to_bit(img.getpixel((x, y))) << 0 | \
        pixel_to_bit(img.getpixel((x, y + 1))) << 1 | \
        pixel_to_bit(img.getpixel((x, y + 2))) << 2 | \
        pixel_to_bit(img.getpixel((x + 1, y))) << 3 | \
        pixel_to_bit(img.getpixel((x + 1, y + 1))) << 4 | \
        pixel_to_bit(img.getpixel((x + 1, y + 2))) << 5 | \
        pixel_to_bit(img.getpixel((x, y + 3))) << 6 | \
        pixel_to_bit(img.getpixel((x + 1, y + 3))) << 7


def byte_to_braille(byt):
    # type: (int) -> str
    byt = minmax(byt, 0, 255)
    return chr(0x2800 + byt)


def image_to_braille(image):
    # type: (PIL.Image) -> List[List[Tixel]]

    # convert the size up to compensate for brail chars being 1/2 wide and
    # 1/4 tall
    new_width = 1 * image.width  # type: int
    new_height = 1 * image.height  # type: int

    # convert the size to a multiple of two and four
    new_width = 2 * math.ceil(new_width / 2)
    new_height = 4 * math.ceil(new_height / 4)

    image = image.resize((new_width, new_height))

    dithered = image.convert('1')  # type: PIL.Image

    lines = []  # type: List[List[Tixel]]

    y: int
    for y in range(math.ceil(dithered.height / 4)):
        line = []  # type: List[Tixel]
        x: int
        for x in range(math.ceil(dithered.width / 2)):
            line.append(Tixel(byte_to_braille(
                pixels_to_byte(dithered, 2 * x, 4 * y)), White, Black))
        lines.append(line)

    return lines


def image_to_braille_high_contrast(image):
    # type: (PIL.Image) -> List[List[Tixel]]
    # convert the size up to compensate for brail chars being 1/2 wide and
    # 1/4 tall
    new_width = 1 * image.width  # type: int
    new_height = 1 * image.height  # type: int

    # convert the size to a multiple of two and four
    new_width = 2 * math.ceil(new_width / 2)
    new_height = 4 * math.ceil(new_height / 4)

    image = image.resize((new_width, new_height))

    quantized = image.quantize(colors=127)  # type: PIL.Image
    dithered = quantized.convert('1')  # type: PIL.Image

    lines = []  # type: List[List[Tixel]]

    y: int
    for y in range(math.ceil(dithered.height / 4)):
        line = []  # type: List[Tixel]
        x: int
        for x in range(math.ceil(dithered.width / 2)):
            line.append(Tixel(byte_to_braille(
                pixels_to_byte(dithered, 2 * x, 4 * y)), White, Black))
        lines.append(line)

    return lines


def pixels_to_color_block_element(image, xcoord, ycoord):
    # type: (PIL.Image, int, int) -> Tixel
    xcoord = max(0, xcoord)
    ycoord = max(0, ycoord)
    top = image.getpixel((xcoord, ycoord))  # type: Tuple[int, int, int]
    bottom = image.getpixel((xcoord, ycoord + 1))  # type: Tuple[int, int, int]
    return Tixel('▀', Color(*top, 255), Color(*bottom, 255))


def image_to_color_block_elements(image):
    # type: (PIL.Image) -> List[List[Tixel]]
    # convert height to a multiple of 2
    new_height = 2 * math.ceil(image.height / 2)  # type: int
    image = image.resize((image.width, new_height))

    # convert to RGB
    image = image.convert('RGB')

    lines = []  # type: List[List[Tixel]]
    y: int
    for y in range(math.ceil(image.height / 2)):
        ycoord = 2 * y  # type: int
        line = []  # type: List[Tixel]
        xcoord = 0  # type: int
        for xcoord in range(image.width):
            line.append(pixels_to_color_block_element(
                image, xcoord, ycoord))
        lines.append(line)

    return lines
