import pytest
import mock

from ..registry import register
from .models import UnsubscribedItem
from ..exceptions import AlreadyRegisteredContent


@mock.patch('content_subscriptions.registry.registry')
def test_register(mock_registry):
    register(UnsubscribedItem)

    assert hasattr(UnsubscribedItem, 'unsubscribeditems')
    mock_registry.append.called_once_with(UnsubscribedItem)


@mock.patch('content_subscriptions.registry.registry')
def test_register_fail(mock_registry):
    fake_registry = []

    def side_effect(model):
        fake_registry.append(model)

    mock_registry.append.side_effect = side_effect
    mock_registry.__contains__.side_effect = lambda x: x in fake_registry

    register(UnsubscribedItem)

    with pytest.raises(AlreadyRegisteredContent):
        register(UnsubscribedItem)
