class AlreadySubscribed(Exception):
    """
    Raised when trying to subscribe when a subscription has already been made.
    """


class UnRegisteredContent(Exception):
    """
    Raised when trying to use a Model as Subscribable content that has not been registered.
    """


class AlreadyRegisteredContent(Exception):
    """
    Raised when a Model has been registered as Subscribable content more than once.
    """
