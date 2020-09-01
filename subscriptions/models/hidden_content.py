from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class HiddenContent(models.Model):
    """
    Model that holds the allows certain subscribable model instances to be hidden from view.
    """

    owner = models.ForeignKey(settings.SUBSCRIPTION_HOLDER_MODEL, related_name='hidden', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ['owner', 'content_type', 'object_id']

    def __str__(self):
        return f'{self.owner.username} is hidding content {self.content_object}'
