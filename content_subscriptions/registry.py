from .managers.subscribable_manager import SubscribableManager
from .exceptions import AlreadyRegisteredContent

registry = []


def register(model):
    """
    Method for registering Subscribable Models to the registry and modfies them with a manager.
    """

    if model in registry:
        raise AlreadyRegisteredContent('This model has already been registered!')

    # Add custom manager
    SubscribableManager().contribute_to_class(model, f'{model._meta.model_name}s')

    registry.append(model)
