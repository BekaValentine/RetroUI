import math
from PIL import Image
from PIL import ImageEnhance


def pixel_to_bit(px):
    return int(px / 255)


def pixels_to_byte(img, x, y):
    return pixel_to_bit(img.getpixel((x, y))) << 0 | \
        pixel_to_bit(img.getpixel((x, y + 1))) << 1 | \
        pixel_to_bit(img.getpixel((x, y + 2))) << 2 | \
        pixel_to_bit(img.getpixel((x + 1, y))) << 3 | \
        pixel_to_bit(img.getpixel((x + 1, y + 1))) << 4 | \
        pixel_to_bit(img.getpixel((x + 1, y + 2))) << 5 | \
        pixel_to_bit(img.getpixel((x, y + 3))) << 6 | \
        pixel_to_bit(img.getpixel((x + 1, y + 3))) << 7


def byte_to_braille(byt):
    return chr(0x2800 + byt)


def image_to_text(image):
    new_width = 2 * math.ceil(image.width / 2)
    new_height = 4 * math.ceil(image.height / 4)
    image = image.resize((new_width, new_height))

    dithered = image.convert('1')

    lines = []

    for y in range(math.ceil(dithered.height / 4)):
        line = ''
        for x in range(math.ceil(dithered.width / 2)):
            line += byte_to_braille(pixels_to_byte(dithered, 2 * x, 4 * y))
        lines.append(line)

    return lines


image = Image.open('grey_cat.jpg')
image = image.resize((int(image.width / 10), int(image.height / 10)))
#image = ImageEnhance.Contrast(image).enhance(3)
image = image.quantize(colors=255)
image.convert('1').show()
image.show()

# image = Image.open('sabocat.png')
# image = image.resize((int(image.width / 3), int(image.height / 3)))

print('\n'.join(image_to_text(image)))
