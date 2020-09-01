from .managers.subscribable_manager import SubscribableManager

registry = []


def register(model):
    if model in registry:
        raise ValueError

    # Add custom manager
    SubscribableManager().contribute_to_class(model, f'{model._meta.model_name}s')

    registry.append(model)
