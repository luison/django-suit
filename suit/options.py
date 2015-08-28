from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from django.db import models
from suit import widgets
from .widgets import SuitTextInputWidget, SuitSelectWidget

__author__ = 'nekmo'

FORMFIELD_FOR_DBFIELD_DEFAULTS[models.CharField] = {'widget': SuitTextInputWidget}
FORMFIELD_FOR_DBFIELD_DEFAULTS[models.ForeignKey] = {'widget': SuitSelectWidget}