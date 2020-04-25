from typing import Optional

from retroui.terminal.event import Event


class ResponderException(BaseException):
    """
    An abstract class for all `Responder`-related exceptions.
    """

    pass


class NoResponderException(ResponderException):
    """
    An exception for when no responder is available for an event.

    `NoResponderException`s have a single slot for the event that caused the
    exception to be thrown.
    """

    __slots__ = ['event']

    def __init__(self, event):
        # type: (Event) -> None
        self.event = event  # type: Event


class Responder(object):
    """
    A `Responder` is an object which can handle input events in some way.

    This includes mouse events, key events, and any other kind of user input.
    """

    def __init__(self):
        # type: () -> None
        pass

    def accepts_first_responder(self):
        # type: () -> bool
        """
        Whether or not the receiver can become the first responder.

        By default, a responder cannot become first responder. Subclasses of
        the `Responder` class can override this method to change whether or
        not they can become first responder and under what conditions they
        will do so.
        """

        return False

    def become_first_responder(self):
        # type: () -> bool
        """
        Perform any setup for acting as first responder, and return whether
        or not the receiver successfully completed all setup steps and is now
        ready to act as first responder.

        By default, no setup is requires, and the receiver can immediately act
        as first responder. Subclasses can override this method to change what
        setup must be performed and determine the success of that process as
        necessary.
        """

        return True

    def resign_first_responder(self):
        # type: () -> bool
        """
        Perform any teardown for having first responder status changed, and
        return whether or not the receiver successfully completed all teardown
        steps and is now ready to give up first responder status.

        By default, no teardown is required, and the receiver can immediately
        give up first responder. Subclasses can override this method to change
        what teardown must be performed and determine the success of that
        process as necessary.
        """

        return True

    def next_responder(self):
        # type: () -> Optional['Responder']
        """
        The next responder in the responder chain that can handle events if
        this one cannot.

        By default, a responder has no next responders, but subclasses can
        override this. For example, when responders are nested hierarchically,
        it's not uncommon for a child responder to return its parent responder
        as its next responder.
        """
        return None

    def no_responder(self, event):
        # type: (Event) -> None
        """
        Perform some action when there is no next responder to pass along an
        event to.

        By default, this throws a `NoResponderException`, but subclasses can
        override this to handle events differently. For example, an
        application may wish to handle such a situation by flashing the screen
        or playing a beep sound to inform the user without throwing an error.
        """

        raise NoResponderException(event)

    def key_press(self, event):
        # type: (Event) -> None
        """
        Handle a key press event.

        By default, key press events are propagated to the next responder if
        there is one, or else they fall off the responder chain.
        """

        nr = self.next_responder()
        if nr:
            nr.key_press(event)
        else:
            self.no_responder(event)
