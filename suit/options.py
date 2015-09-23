__author__ = 'nekmo'
from django.core.exceptions import ImproperlyConfigured
try:
    from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
    from django.db import models
    from .widgets import SuitTextInputWidget, SuitIntegerWidget, AutosizedTextarea
except ImproperlyConfigured:
    pass
else:
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.CharField] = {'widget': SuitTextInputWidget}
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.IntegerField] = {'widget': SuitIntegerWidget}
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.TextField] = {'widget': AutosizedTextarea}
    # FORMFIELD_FOR_DBFIELD_DEFAULTS[models.ForeignKey] = {'widget': SuitSelectWidget}