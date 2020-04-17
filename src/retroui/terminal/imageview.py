from retroui.terminal.view import *


class ImageView(View):
    """
    An `ImageView` displays an image rendered as text.

    The following rendering techniques are available:

        `'dither'`
            Renders to a black-and-white dithered image represented by 8-dot
            Braille characters.

        `'dither2'`
            Renders to a black-and-white dithered image represented by 8-dot
            Braille characters, but with greater contrast between lights and
            darks. Works better for images with relatively even brightness.

        `'color'`
            Renders to a possibly full color image using block element
            characters. Default.

    Slots:

        `image`
            The unaltered image displayed in the `ImageView`.

        `_scaled_image`
            A scaled version of the image to actually display in the rendered
            `ImageView`.

        `scale`
            The scale at which to render the image.

        `rendering_technique`
            The rendering technique used to display the image.

        `_render_lines`
            The cached rendering of the image.

        `_cache`
            A cache of the images at different scales and rendering techniques.
    """

    __slots__ = ['image', '_scaled_image', 'scale',
                 'rendering_technique', '_render_lines', '_cache']

    def __init__(self):
        self.image = None
        self._scaled_image = None
        self.scale = 1.0
        self.rendering_technique = 'color'
        self._render_lines = None
        self._cache = None

    def set_rendering_technique(self, technique):
        if technique in ['dither', 'dither2', 'color']:
            self.rendering_technique = technique

        else:
            self.rendering_technique = 'color'
        self.render_image()

    def set_image(self, img):
        self.image = img
        self._render_lines = []
        self._cache = {}
        self.render_image()

    def set_scale(self, new_scale):
        self.scale = max(0.0, float(new_scale))
        self.render_image()

    def render_image(self):
        cache_id = (self.rendering_technique, self.scale)
        if cache_id not in self._cache:

            if self.rendering_technique == 'color':
                hfrac = 1 / 8
                vfrac = 2 / 17
                self._scaled_image = self.image.image_by_resizing(
                    Size(hfrac * self.scale * self.image.size.width, vfrac * self.scale * self.image.size.height))
                render = self._scaled_image.color_representation()

            elif self.rendering_technique == 'dither':
                hfrac = 2 / 8
                vfrac = 4 / 17
                self._scaled_image = self.image.image_by_resizing(
                    Size(hfrac * self.scale * self.image.size.width, vfrac * self.scale * self.image.size.height))
                render = self._scaled_image.braille_representation()

            elif self.rendering_technique == 'dither2':
                hfrac = 2 / 8
                vfrac = 4 / 17
                self._scaled_image = self.image.image_by_resizing(
                    Size(hfrac * self.scale * self.image.size.width, vfrac * self.scale * self.image.size.height))
                render = self._scaled_image.braille_representation_high_contrast()

            self._cache[cache_id] = render

        self._render_lines = self._cache[cache_id]
        self.set_size(
            Size(max([len(line) for line in self._render_lines]), len(self._render_lines)))

    def key_press(self, ev):
        if ev.key_code == '+' or ev.key_code == '=':
            self.set_scale(self.scale + 0.1)

        elif ev.key_code == '-':
            self.set_scale(self.scale - 0.1)

        elif ev.key_code == '0':
            self.set_scale(1.0)

        elif ev.key_code == 'm':
            m = self.rendering_technique
            rep = {
                'dither': 'dither2',
                'dither2': 'color',
                'color': 'dither'
            }

            self.set_rendering_technique(rep[m])

        else:
            super().key_press(ev)

    def draw(self):
        return self._render_lines
