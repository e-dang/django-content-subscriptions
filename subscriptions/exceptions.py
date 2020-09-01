class AlreadySubscribed(Exception):
    """
    Raised when trying to subscribe when a subscription has already been made.
    """


class UnRegisteredContent(Exception):
    """
    Raised when trying to use a Model as Subscribable content that has not been registered.
    """
