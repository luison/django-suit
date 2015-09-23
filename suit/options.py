from django.core.exceptions import ImproperlyConfigured
try:
    from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
except ImproperlyConfigured:
    pass
from django.db import models
from .widgets import SuitTextInputWidget, SuitIntegerWidget, AutosizedTextarea

__author__ = 'nekmo'

FORMFIELD_FOR_DBFIELD_DEFAULTS[models.CharField] = {'widget': SuitTextInputWidget}
FORMFIELD_FOR_DBFIELD_DEFAULTS[models.IntegerField] = {'widget': SuitIntegerWidget}
FORMFIELD_FOR_DBFIELD_DEFAULTS[models.TextField] = {'widget': AutosizedTextarea}
# FORMFIELD_FOR_DBFIELD_DEFAULTS[models.ForeignKey] = {'widget': SuitSelectWidget}