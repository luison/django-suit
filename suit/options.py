from django.conf import settings

from suit.widgets import SuitSplitDateTimeWidget, SuitDateWidget, SuitTimeWidget

__author__ = 'nekmo'
try:
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    ImproperlyConfigured = ImportError
try:
    from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
    from django.db import models
    from .widgets import SuitTextInputWidget, SuitIntegerWidget, AutosizedTextarea
except ImproperlyConfigured:
    pass
else:
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.CharField] = {'widget': SuitTextInputWidget}
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.IntegerField] = {'widget': SuitIntegerWidget}
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.DateTimeField] = {'widget': SuitSplitDateTimeWidget}
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.DateField] = {'widget': SuitDateWidget}
    FORMFIELD_FOR_DBFIELD_DEFAULTS[models.TimeField] = {'widget': SuitTimeWidget}
    # FORMFIELD_FOR_DBFIELD_DEFAULTS[models.ForeignKey] = {'widget': SuitSelectWidget}