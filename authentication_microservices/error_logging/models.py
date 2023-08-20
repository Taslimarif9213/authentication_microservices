import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

LOG_LEVELS = (
    (logging.NOTSET, _('NotSet')),
    (logging.INFO, _('Info')),
    (logging.WARNING, _('Warning')),
    (logging.DEBUG, _('Debug')),
    (logging.ERROR, _('Error')),
    (logging.FATAL, _('Fatal')),
)


class StatusLog(models.Model):
    class Meta:
        ordering = ('-create_datetime',)
        verbose_name_plural = verbose_name = 'Logging'
        db_table = 'error_logging'

    logger_name = models.TextField()
    level = models.PositiveSmallIntegerField(choices=LOG_LEVELS, default=logging.ERROR, db_index=True)
    msg = models.TextField()
    trace = models.TextField(blank=True, null=True)
    error_code = models.CharField(null=True, max_length=255)
    method_name = models.CharField(null=True, max_length=255)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
