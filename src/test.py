from retroui.terminal.event import *
from retroui.terminal.color import *
from retroui.terminal.tixel import *
from retroui.terminal.application import *
from retroui.terminal.size import *
from retroui.terminal.view import *
from retroui.terminal.textview import *
from retroui.terminal.clipview import *
from retroui.terminal.fillview import *
from retroui.terminal.imageview import *
from retroui.terminal.scrollview import *
from retroui.terminal.splitview import *
from retroui.terminal.barindicator import *
from retroui.terminal.textfoldview import *
from retroui.terminal.slider import *
from retroui.terminal.listview import *
from retroui.terminal.box import *
from retroui.terminal.accordionview import *
from retroui.terminal.tabview import *
from retroui.terminal.stepper import *
from retroui.terminal.button import *
from retroui.terminal.colorswatch import *
from retroui.terminal.textfield import *
from retroui.terminal.panel import *
from retroui.terminal.point import *
from retroui.terminal.image import *


class MyApp(Application):

    def test_accordion_view(self):
        # type: () -> None
        text_view = TextView()
        text_view.set_line_break_width(100)
        text_view.set_text('''--- BEGIN ---
The origins of cyberpunk are rooted in the New Wave science fiction movement of the 1960s and 70s, where New Worlds, under the editorship of Michael Moorcock, began inviting and encouraging stories that examined new writing styles, techniques, and archetypes. Reacting to conventional storytelling, New Wave authors attempted to present a world where society coped with a constant upheaval of new technology and culture, generally with dystopian outcomes. Writers like Roger Zelazny, J.G. Ballard, Philip Jose Farmer, and Harlan Ellison often examined the impact of drug culture, technology, and the sexual revolution with an avant-garde style influenced by the Beat Generation (especially William S. Burroughs' own SF), Dadaism, and their own ideas.[14] Ballard attacked the idea that stories should follow the "archetypes" popular since the time of Ancient Greece, and the assumption that these would somehow be the same ones that would call to modern readers, as Joseph Campbell argued in The Hero with a Thousand Faces. Instead, Ballard wanted to write a new myth for the modern reader, a style with "more psycho-literary ideas, more meta-biological and meta-chemical concepts, private time systems, synthetic psychologies and space-times, more of the sombre half-worlds one glimpses in the paintings of schizophrenics."[15]

This had a profound influence on a new generation of writers, some of whom would come to call their movement "Cyberpunk". One, Bruce Sterling, later said:

In the circle of American science fiction writers of my generation — cyberpunks and humanists and so forth — [Ballard] was a towering figure. We used to have bitter struggles over who was more Ballardian than whom. We knew we were not fit to polish the man’s boots, and we were scarcely able to understand how we could get to a position to do work which he might respect or stand, but at least we were able to see the peak of achievement that he had reached.[16]
--- END ---''')

        text_view_2 = TextView()
        text_view_2.set_line_break_width(100)
        text_view_2.set_text('''--- BEGIN ---
Ballard, Zelazny, and the rest of New Wave was seen by the subsequent generation as delivering more "realism" to science fiction, and they attempted to build on this.

Similarly influential, and generally cited as proto-cyberpunk, is the Philip K. Dick novel Do Androids Dream of Electric Sheep, first published in 1968. Presenting precisely the general feeling of dystopian post-economic-apocalyptic future as Gibson and Sterling later deliver, it examines ethical and moral problems with cybernetic, artificial intelligence in a way more "realist" than the Isaac Asimov Robot series that laid its philosophical foundation. Dick's protege and friend K. W. Jeter wrote a very dark and imaginative novel called Dr. Adder in 1972 that, Dick lamented, might have been more influential in the field had it been able to find a publisher at that time.[citation needed] It was not published until 1984, after which Jeter made it the first book in a trilogy, followed by The Glass Hammer (1985) and Death Arms (1987). Jeter wrote other standalone cyberpunk novels before going on to write three authorized sequels to Do Androids Dream of electric sheep, named Blade Runner 2: The Edge of Human (1995), Blade Runner 3: Replicant Night (1996), and Blade Runner 4: Eye and Talon.
--- END ---''')

        text_view_3 = TextView()
        text_view_3.set_line_break_width(100)
        text_view_3.set_text('''--- BEGIN ---
Do Androids Dream of Electric Sheep was made into the seminal movie Blade Runner, released in 1982. This was one year after William Gibson's story, "Johnny Mnemonic" helped move proto-cyberpunk concepts into the mainstream. That story, which also became a film years later in 1995, involves another dystopian future, where human couriers deliver computer data, stored cybernetically in their own minds.

In 1983 a short story written by Bruce Bethke, called Cyberpunk, was published in Amazing Stories. The term was picked up by Gardner Dozois, editor of Isaac Asimov's Science Fiction Magazine and popularized in his editorials. Bethke says he made two lists of words, one for technology, one for troublemakers, and experimented with combining them variously into compound words, consciously attempting to coin a term that encompassed both punk attitudes and high technology.
--- END ---''')

        accordion_view = AccordionView()
        accordion_view.set_size(Size(100, 100))
        accordion_view.set_views([
            ('part 1', text_view),
            ('part 2', text_view_2),
            ('part 3', text_view_3),
        ])
        accordion_view.set_allows_multiple_expansions(True)

        self.set_main_view(accordion_view)
        self.set_first_responder(accordion_view)

    def test_bar_indicator(self):
        # type: () -> None
        bar_indicator = BarIndicator()
        bar_indicator.set_is_vertical(False)
        bar_indicator.set_readout_position('beginning')
        bar_indicator.set_readout_formatter(lambda v: 5 * str(v))
        bar_indicator.set_readout_size(30)
        self.set_main_view(bar_indicator)

    def test_box(self):
        # type: () -> None

        text_view = TextView()
        text_view.set_line_break_width(100)
        text_view.set_text('''--- BEGIN ---
The origins of cyberpunk are rooted in the New Wave science fiction movement of the 1960s and 70s, where New Worlds, under the editorship of Michael Moorcock, began inviting and encouraging stories that examined new writing styles, techniques, and archetypes. Reacting to conventional storytelling, New Wave authors attempted to present a world where society coped with a constant upheaval of new technology and culture, generally with dystopian outcomes. Writers like Roger Zelazny, J.G. Ballard, Philip Jose Farmer, and Harlan Ellison often examined the impact of drug culture, technology, and the sexual revolution with an avant-garde style influenced by the Beat Generation (especially William S. Burroughs' own SF), Dadaism, and their own ideas.[14] Ballard attacked the idea that stories should follow the "archetypes" popular since the time of Ancient Greece, and the assumption that these would somehow be the same ones that would call to modern readers, as Joseph Campbell argued in The Hero with a Thousand Faces. Instead, Ballard wanted to write a new myth for the modern reader, a style with "more psycho-literary ideas, more meta-biological and meta-chemical concepts, private time systems, synthetic psychologies and space-times, more of the sombre half-worlds one glimpses in the paintings of schizophrenics."[15]

This had a profound influence on a new generation of writers, some of whom would come to call their movement "Cyberpunk". One, Bruce Sterling, later said:

In the circle of American science fiction writers of my generation — cyberpunks and humanists and so forth — [Ballard] was a towering figure. We used to have bitter struggles over who was more Ballardian than whom. We knew we were not fit to polish the man’s boots, and we were scarcely able to understand how we could get to a position to do work which he might respect or stand, but at least we were able to see the peak of achievement that he had reached.[16]
--- END ---''')

        box = Box()
        self.set_main_view(box)
        box.set_content_view(text_view)
        box.set_title('This is a box!')
        box.set_title_style('full_width_bar')
        box.set_title_alignment('center')

    def test_button(self):
        button = Button()
        button.set_style('on_off')
        button.set_label(repr(button.state))
        button.set_label_location('left')
        self.set_main_view(button)
        self.set_first_responder(button)

        def callback():
            button.set_label(repr(button.state))
            pass
        button.set_callback(callback)

    def test_color_swatch(self):
        color_swatch = ColorSwatch()
        color_swatch.set_color(Color(127, 0, 255, 255))
        self.set_main_view(color_swatch)

    def test_empty_view(self):
        # type: () -> None
        empty_view = EmptyView()
        self.set_main_view(empty_view)

    def test_fill_view(self):
        # type: () -> None
        fill_view = FillView()
        fill_view.set_fill_character('#')
        self.set_main_view(fill_view)

    def test_image_view(self):
        img = Image('mona_lisa.jpg')
        image_view = ImageView()
        image_view.set_image(img)
        image_view.set_rendering_technique('dither')
        self.set_first_responder(image_view)
        self.set_main_view(image_view)

    def test_list_view(self):
        # type: () -> None
        list_view = ListView()
        list_view.set_list([
            Tree('foo', []),
            Tree('bar', [
                Tree('bar-1', [
                    Tree('bar-1-1', []),
                    Tree('bar-1-2', [])
                ]),
                Tree('bar-2', [
                    Tree('bar-2-1', []),
                    Tree('bar-2-2', [])
                ])
            ]),
            Tree('baz', [])
        ])
        list_view.expand_all()
        self.set_first_responder(list_view)
        self.set_main_view(list_view)

    def test_panel(self):
        # type: () -> None
        main_panel = Panel()
        main_panel.set_title(
            'This is a really long title for a fairly small panel but there you have it!')
        main_panel.set_background_color(Red)
        self.set_main_panel(main_panel)
        self.set_key_panel(main_panel)

        text_view = TextView()
        text_view.set_line_break_width(50)
        text_view.set_text('''--- BEGIN ---
The origins of cyberpunk are rooted in the New Wave science fiction movement of the 1960s and 70s, where New Worlds, under the editorship of Michael Moorcock, began inviting and encouraging stories that examined new writing styles, techniques, and archetypes. Reacting to conventional storytelling, New Wave authors attempted to present a world where society coped with a constant upheaval of new technology and culture, generally with dystopian outcomes. Writers like Roger Zelazny, J.G. Ballard, Philip Jose Farmer, and Harlan Ellison often examined the impact of drug culture, technology, and the sexual revolution with an avant-garde style influenced by the Beat Generation (especially William S. Burroughs' own SF), Dadaism, and their own ideas.[14] Ballard attacked the idea that stories should follow the "archetypes" popular since the time of Ancient Greece, and the assumption that these would somehow be the same ones that would call to modern readers, as Joseph Campbell argued in The Hero with a Thousand Faces. Instead, Ballard wanted to write a new myth for the modern reader, a style with "more psycho-literary ideas, more meta-biological and meta-chemical concepts, private time systems, synthetic psychologies and space-times, more of the sombre half-worlds one glimpses in the paintings of schizophrenics."[15]

This had a profound influence on a new generation of writers, some of whom would come to call their movement "Cyberpunk". One, Bruce Sterling, later said:

In the circle of American science fiction writers of my generation — cyberpunks and humanists and so forth — [Ballard] was a towering figure. We used to have bitter struggles over who was more Ballardian than whom. We knew we were not fit to polish the man’s boots, and we were scarcely able to understand how we could get to a position to do work which he might respect or stand, but at least we were able to see the peak of achievement that he had reached.[16]

Ballard, Zelazny, and the rest of New Wave was seen by the subsequent generation as delivering more "realism" to science fiction, and they attempted to build on this.

Similarly influential, and generally cited as proto-cyberpunk, is the Philip K. Dick novel Do Androids Dream of Electric Sheep, first published in 1968. Presenting precisely the general feeling of dystopian post-economic-apocalyptic future as Gibson and Sterling later deliver, it examines ethical and moral problems with cybernetic, artificial intelligence in a way more "realist" than the Isaac Asimov Robot series that laid its philosophical foundation. Dick's protege and friend K. W. Jeter wrote a very dark and imaginative novel called Dr. Adder in 1972 that, Dick lamented, might have been more influential in the field had it been able to find a publisher at that time.[citation needed] It was not published until 1984, after which Jeter made it the first book in a trilogy, followed by The Glass Hammer (1985) and Death Arms (1987). Jeter wrote other standalone cyberpunk novels before going on to write three authorized sequels to Do Androids Dream of electric sheep, named Blade Runner 2: The Edge of Human (1995), Blade Runner 3: Replicant Night (1996), and Blade Runner 4: Eye and Talon.

Do Androids Dream of Electric Sheep was made into the seminal movie Blade Runner, released in 1982. This was one year after William Gibson's story, "Johnny Mnemonic" helped move proto-cyberpunk concepts into the mainstream. That story, which also became a film years later in 1995, involves another dystopian future, where human couriers deliver computer data, stored cybernetically in their own minds.

In 1983 a short story written by Bruce Bethke, called Cyberpunk, was published in Amazing Stories. The term was picked up by Gardner Dozois, editor of Isaac Asimov's Science Fiction Magazine and popularized in his editorials. Bethke says he made two lists of words, one for technology, one for troublemakers, and experimented with combining them variously into compound words, consciously attempting to coin a term that encompassed both punk attitudes and high technology.
--- END ---''')

        scroll_view = ScrollView()
        scroll_view.set_autohides_scrollers(True)
        main_panel.set_content_view(scroll_view)
        scroll_view.set_document_view(text_view)
        main_panel.set_first_responder(scroll_view)

        non_main_panel = Panel()
        non_main_panel.set_size(Size(20, 20))
        non_main_panel.set_location(Point(5, 5))
        non_main_panel.set_title('Panel 1')
        non_main_panel.set_background_color(Red)
        self.add_panel(non_main_panel)

        non_main_panel2 = Panel()
        non_main_panel2.set_size(Size(10, 50))
        non_main_panel2.set_location(Point(10, 10))
        non_main_panel2.set_title('Panel 2')
        non_main_panel2.set_background_color(Blue)
        self.add_panel(non_main_panel2)

    def test_scroll_view(self):
        # type: () -> None
        text_view = TextView()
        text_view.set_line_break_width(50)
        text_view.set_text('''--- BEGIN ---
The origins of cyberpunk are rooted in the New Wave science fiction movement of the 1960s and 70s, where New Worlds, under the editorship of Michael Moorcock, began inviting and encouraging stories that examined new writing styles, techniques, and archetypes. Reacting to conventional storytelling, New Wave authors attempted to present a world where society coped with a constant upheaval of new technology and culture, generally with dystopian outcomes. Writers like Roger Zelazny, J.G. Ballard, Philip Jose Farmer, and Harlan Ellison often examined the impact of drug culture, technology, and the sexual revolution with an avant-garde style influenced by the Beat Generation (especially William S. Burroughs' own SF), Dadaism, and their own ideas.[14] Ballard attacked the idea that stories should follow the "archetypes" popular since the time of Ancient Greece, and the assumption that these would somehow be the same ones that would call to modern readers, as Joseph Campbell argued in The Hero with a Thousand Faces. Instead, Ballard wanted to write a new myth for the modern reader, a style with "more psycho-literary ideas, more meta-biological and meta-chemical concepts, private time systems, synthetic psychologies and space-times, more of the sombre half-worlds one glimpses in the paintings of schizophrenics."[15]

This had a profound influence on a new generation of writers, some of whom would come to call their movement "Cyberpunk". One, Bruce Sterling, later said:

In the circle of American science fiction writers of my generation — cyberpunks and humanists and so forth — [Ballard] was a towering figure. We used to have bitter struggles over who was more Ballardian than whom. We knew we were not fit to polish the man’s boots, and we were scarcely able to understand how we could get to a position to do work which he might respect or stand, but at least we were able to see the peak of achievement that he had reached.[16]

Ballard, Zelazny, and the rest of New Wave was seen by the subsequent generation as delivering more "realism" to science fiction, and they attempted to build on this.

Similarly influential, and generally cited as proto-cyberpunk, is the Philip K. Dick novel Do Androids Dream of Electric Sheep, first published in 1968. Presenting precisely the general feeling of dystopian post-economic-apocalyptic future as Gibson and Sterling later deliver, it examines ethical and moral problems with cybernetic, artificial intelligence in a way more "realist" than the Isaac Asimov Robot series that laid its philosophical foundation. Dick's protege and friend K. W. Jeter wrote a very dark and imaginative novel called Dr. Adder in 1972 that, Dick lamented, might have been more influential in the field had it been able to find a publisher at that time.[citation needed] It was not published until 1984, after which Jeter made it the first book in a trilogy, followed by The Glass Hammer (1985) and Death Arms (1987). Jeter wrote other standalone cyberpunk novels before going on to write three authorized sequels to Do Androids Dream of electric sheep, named Blade Runner 2: The Edge of Human (1995), Blade Runner 3: Replicant Night (1996), and Blade Runner 4: Eye and Talon.

Do Androids Dream of Electric Sheep was made into the seminal movie Blade Runner, released in 1982. This was one year after William Gibson's story, "Johnny Mnemonic" helped move proto-cyberpunk concepts into the mainstream. That story, which also became a film years later in 1995, involves another dystopian future, where human couriers deliver computer data, stored cybernetically in their own minds.

In 1983 a short story written by Bruce Bethke, called Cyberpunk, was published in Amazing Stories. The term was picked up by Gardner Dozois, editor of Isaac Asimov's Science Fiction Magazine and popularized in his editorials. Bethke says he made two lists of words, one for technology, one for troublemakers, and experimented with combining them variously into compound words, consciously attempting to coin a term that encompassed both punk attitudes and high technology.
--- END ---''')

        scroll_view = ScrollView()
        scroll_view.set_autohides_scrollers(True)
        self.set_main_view(scroll_view)
        scroll_view.set_document_view(text_view)
        self.set_first_responder(scroll_view)

    def test_slider(self):
        # type: () -> None
        slider = Slider()
        self.set_first_responder(slider)
        # self.slider.set_is_vertical(True)
        slider.set_size(Size(20, 20))
        slider.set_divisions(4)
        self.set_main_view(slider)
        self.set_first_responder(slider)

    def test_split_view(self):
        # type: () -> None
        fv0 = FillView()
        fv0.set_fill_character('#')

        fv1 = FillView()
        fv1.set_fill_character('.')

        split_view = SplitView()
        split_view.set_first_subview(fv0)
        split_view.set_second_subview(fv1)\

        self.set_main_view(split_view)
        self.set_first_responder(split_view)

    def test_stepper(self):
        # type: () -> None
        stepper = Stepper()
        stepper.set_minimum_value(0)
        stepper.set_maximum_value(10)
        self.set_main_view(stepper)
        self.set_first_responder(stepper)

    def test_tab_view(self):
        # type: () -> None
        text_view = TextView()
        text_view.set_line_break_width(100)
        text_view.set_text('''--- BEGIN ---
The origins of cyberpunk are rooted in the New Wave science fiction movement of the 1960s and 70s, where New Worlds, under the editorship of Michael Moorcock, began inviting and encouraging stories that examined new writing styles, techniques, and archetypes. Reacting to conventional storytelling, New Wave authors attempted to present a world where society coped with a constant upheaval of new technology and culture, generally with dystopian outcomes. Writers like Roger Zelazny, J.G. Ballard, Philip Jose Farmer, and Harlan Ellison often examined the impact of drug culture, technology, and the sexual revolution with an avant-garde style influenced by the Beat Generation (especially William S. Burroughs' own SF), Dadaism, and their own ideas.[14] Ballard attacked the idea that stories should follow the "archetypes" popular since the time of Ancient Greece, and the assumption that these would somehow be the same ones that would call to modern readers, as Joseph Campbell argued in The Hero with a Thousand Faces. Instead, Ballard wanted to write a new myth for the modern reader, a style with "more psycho-literary ideas, more meta-biological and meta-chemical concepts, private time systems, synthetic psychologies and space-times, more of the sombre half-worlds one glimpses in the paintings of schizophrenics."[15]

This had a profound influence on a new generation of writers, some of whom would come to call their movement "Cyberpunk". One, Bruce Sterling, later said:

In the circle of American science fiction writers of my generation — cyberpunks and humanists and so forth — [Ballard] was a towering figure. We used to have bitter struggles over who was more Ballardian than whom. We knew we were not fit to polish the man’s boots, and we were scarcely able to understand how we could get to a position to do work which he might respect or stand, but at least we were able to see the peak of achievement that he had reached.[16]
--- END ---''')

        text_view_2 = TextView()
        text_view_2.set_line_break_width(100)
        text_view_2.set_text('''--- BEGIN ---
Ballard, Zelazny, and the rest of New Wave was seen by the subsequent generation as delivering more "realism" to science fiction, and they attempted to build on this.

Similarly influential, and generally cited as proto-cyberpunk, is the Philip K. Dick novel Do Androids Dream of Electric Sheep, first published in 1968. Presenting precisely the general feeling of dystopian post-economic-apocalyptic future as Gibson and Sterling later deliver, it examines ethical and moral problems with cybernetic, artificial intelligence in a way more "realist" than the Isaac Asimov Robot series that laid its philosophical foundation. Dick's protege and friend K. W. Jeter wrote a very dark and imaginative novel called Dr. Adder in 1972 that, Dick lamented, might have been more influential in the field had it been able to find a publisher at that time.[citation needed] It was not published until 1984, after which Jeter made it the first book in a trilogy, followed by The Glass Hammer (1985) and Death Arms (1987). Jeter wrote other standalone cyberpunk novels before going on to write three authorized sequels to Do Androids Dream of electric sheep, named Blade Runner 2: The Edge of Human (1995), Blade Runner 3: Replicant Night (1996), and Blade Runner 4: Eye and Talon.
--- END ---''')

        text_view_3 = TextView()
        text_view_3.set_line_break_width(100)
        text_view_3.set_text('''--- BEGIN ---
Do Androids Dream of Electric Sheep was made into the seminal movie Blade Runner, released in 1982. This was one year after William Gibson's story, "Johnny Mnemonic" helped move proto-cyberpunk concepts into the mainstream. That story, which also became a film years later in 1995, involves another dystopian future, where human couriers deliver computer data, stored cybernetically in their own minds.

In 1983 a short story written by Bruce Bethke, called Cyberpunk, was published in Amazing Stories. The term was picked up by Gardner Dozois, editor of Isaac Asimov's Science Fiction Magazine and popularized in his editorials. Bethke says he made two lists of words, one for technology, one for troublemakers, and experimented with combining them variously into compound words, consciously attempting to coin a term that encompassed both punk attitudes and high technology.
--- END ---''')

        tab_view = TabView()
        tab_view.set_size(Size(100, 50))
        tab_view.set_views([
            ('part 1', text_view),
            ('part 2', text_view_2),
            ('part 3', text_view_3),
        ])
        tab_view.set_tab_style('fill_center')

        self.set_main_view(tab_view)
        self.set_first_responder(tab_view)

    def test_text_field(self):
        # type: () -> None
        text_field = TextField()
        text_field.set_text('''--- BEGIN ---
The origins of cyberpunk are rooted in the New Wave science fiction movement of the 1960s and 70s, where New Worlds, under the editorship of Michael Moorcock.

This had a profound influence on a new generation of writers, some of whom would come to call their movement "Cyberpunk". One, Bruce Sterling, later said:
In the circle of American science fiction writers of my generation — cyberpunks and humanists and so forth — [Ballard] was a towering figure. We used to have bitter struggles over who was more Ballardian than whom. We knew we were not fit to polish the man’s boots, and we were scarcely able to understand how we could get to a position to do work which he might respect or stand, but at least we were able to see the peak of achievement that he had reached.[16]
--- END ---''')
        text_field.set_cursor_position(0, 0)
        text_field.set_size(Size(50, 20))
        cv = ClipView()
        cv.set_document_view(text_field)
        self.set_main_view(cv)
        self.set_first_responder(text_field)

    def test_text_view(self):
        # type: () -> None

        text_view = TextView()
        text_view.set_line_break_width(100)
        text_view.set_text('''--- BEGIN ---
The origins of cyberpunk are rooted in the New Wave science fiction movement of the 1960s and 70s, where New Worlds, under the editorship of Michael Moorcock, began inviting and encouraging stories that examined new writing styles, techniques, and archetypes. Reacting to conventional storytelling, New Wave authors attempted to present a world where society coped with a constant upheaval of new technology and culture, generally with dystopian outcomes. Writers like Roger Zelazny, J.G. Ballard, Philip Jose Farmer, and Harlan Ellison often examined the impact of drug culture, technology, and the sexual revolution with an avant-garde style influenced by the Beat Generation (especially William S. Burroughs' own SF), Dadaism, and their own ideas.[14] Ballard attacked the idea that stories should follow the "archetypes" popular since the time of Ancient Greece, and the assumption that these would somehow be the same ones that would call to modern readers, as Joseph Campbell argued in The Hero with a Thousand Faces. Instead, Ballard wanted to write a new myth for the modern reader, a style with "more psycho-literary ideas, more meta-biological and meta-chemical concepts, private time systems, synthetic psychologies and space-times, more of the sombre half-worlds one glimpses in the paintings of schizophrenics."[15]

This had a profound influence on a new generation of writers, some of whom would come to call their movement "Cyberpunk". One, Bruce Sterling, later said:

In the circle of American science fiction writers of my generation — cyberpunks and humanists and so forth — [Ballard] was a towering figure. We used to have bitter struggles over who was more Ballardian than whom. We knew we were not fit to polish the man’s boots, and we were scarcely able to understand how we could get to a position to do work which he might respect or stand, but at least we were able to see the peak of achievement that he had reached.[16]
--- END ---''')

        self.set_main_view(text_view)

    def test_text_fold_view(self):
        # type: () -> None

        text_fold_view = TextFoldView()
        text_fold_view.set_size(Size(100, 50))
        text_fold_view.set_folded_text('''--- BEGIN ---
The origins of cyberpunk are rooted in the New Wave science fiction movement of the 1960s and 70s, where New Worlds, under the editorship of Michael Moorcock, began inviting and encouraging stories that examined new writing styles, techniques, and archetypes. Reacting to conventional storytelling, New Wave authors attempted to present a world where society coped with a constant upheaval of new technology and culture, generally with dystopian outcomes. Writers like Roger Zelazny, J.G. Ballard, Philip Jose Farmer, and Harlan Ellison often examined the impact of drug culture, technology, and the sexual revolution with an avant-garde style influenced by the Beat Generation (especially William S. Burroughs' own SF), Dadaism, and their own ideas.[14] Ballard attacked the idea that stories should follow the "archetypes" popular since the time of Ancient Greece, and the assumption that these would somehow be the same ones that would call to modern readers, as Joseph Campbell argued in The Hero with a Thousand Faces. Instead, Ballard wanted to write a new myth for the modern reader, a style with "more psycho-literary ideas, more meta-biological and meta-chemical concepts, private time systems, synthetic psychologies and space-times, more of the sombre half-worlds one glimpses in the paintings of schizophrenics."[15]

This had a profound influence on a new generation of writers, some of whom would come to call their movement "Cyberpunk". One, Bruce Sterling, later said:

In the circle of American science fiction writers of my generation — cyberpunks and humanists and so forth — [Ballard] was a towering figure. We used to have bitter struggles over who was more Ballardian than whom. We knew we were not fit to polish the man’s boots, and we were scarcely able to understand how we could get to a position to do work which he might respect or stand, but at least we were able to see the peak of achievement that he had reached.[16]
--- END ---''')
        self.set_first_responder(text_fold_view)
        self.set_main_view(text_fold_view)

    def on_run(self):
        # type: () -> None

        # self.test_empty_view()
        # self.test_fill_view()
        # self.test_split_view()
        # self.test_text_view()
        # self.test_text_fold_view()
        # self.test_tab_view()
        # self.test_box()
        # self.test_accordion_view()
        # self.test_bar_indicator()
        # self.test_scroll_view()
        # self.test_list_view()
        # self.test_slider()
        # self.test_image_view()
        # self.test_stepper()
        # self.test_button()
        # self.test_color_swatch()
        # self.test_text_field()
        self.test_panel()

    def key_press(self, ev):
        # type: (Event) -> None:
        self.set_debug(False)
        pass


MyApp().run()
