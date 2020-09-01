import pytest
import mock

from ..registry import register
from .models import UnsubscribedItem


@mock.patch('subscriptions.registry.registry')
def test_register(mock_registry):
    register(UnsubscribedItem)

    assert hasattr(UnsubscribedItem, 'unsubscribeditems')
    mock_registry.append.called_once_with(UnsubscribedItem)


@mock.patch('subscriptions.registry.registry')
def test_register_fail(mock_registry):
    mock_registry.append.side_effect = [None, ValueError]

    register(UnsubscribedItem)

    with pytest.raises(ValueError):
        register(UnsubscribedItem)
