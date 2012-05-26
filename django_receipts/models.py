from datetime import datetime

from django.db import models

from django_receipts import constants


class Receipt(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    checked = models.DateTimeField(default=None, blank=True, null=True)
    hash = models.CharField(max_length=255, unique=True)
    valid = models.IntegerField(choices=constants.VALID,
                                default=constants.UNCHECKED)
    allow = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
        db_table = 'receipts'

    def unicode(self):
        return self.hash

    def get_status(self):
        if not self.allow:
            return 'invalid'
        return constants.VALID_INVERTED[self.valid]
