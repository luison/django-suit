from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget, AdminTextInputWidget, AdminIntegerFieldWidget, \
    AdminTextareaWidget
from django.forms import TextInput, Select, Textarea, CheckboxSelectMultiple
from django.forms.widgets import ChoiceFieldRenderer, CheckboxChoiceInput
from django.utils.safestring import mark_safe
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.admin.templatetags.admin_static import static

# todo eliminar, no debemos meter un -sm a todos
DEFAULT_INPUT_SIZE = ''


class SuitFormComponentMix(object):
    def render(self, name, value, attrs=None):
        final_attrs = {'class': 'form-control bs2-retro %s' % DEFAULT_INPUT_SIZE}
        if attrs is not None:
            final_attrs['class'] = ' '.join((attrs.get('class', ''), final_attrs['class']))
            if attrs.get('class'):
                del attrs['class']
            final_attrs.update(attrs)
        response = super(SuitFormComponentMix, self).render(name, value, final_attrs)
        return response


class NumberInput(TextInput):
    """
    HTML5 Number input
    Left for backwards compatibility
    """
    input_type = 'number'


class HTML5Input(TextInput):
    """
    Supports any HTML5 input
    http://www.w3schools.com/html/html5_form_input_types.asp
    """

    def __init__(self, attrs=None, input_type=None):
        self.input_type = input_type
        super(HTML5Input, self).__init__(attrs)


#
class LinkedSelect(Select):
    """
    Linked select - Adds link to foreign item, when used with foreign key field
    """

    def __init__(self, attrs=None, choices=()):
        attrs = _make_attrs(attrs, classes="linked-select 'form-control bs2-retro %s" % DEFAULT_INPUT_SIZE)
        super(LinkedSelect, self).__init__(attrs, choices)


class EnclosedInput(TextInput):
    """
    Widget for bootstrap appended/prepended inputs
    """

    def __init__(self, attrs=None, prepend=None, append=None):
        """
        For prepend, append parameters use string like %, $ or html
        """
        self.prepend = prepend
        self.append = append
        # recover previous class attr and add bs3
        if attrs is None:
            attrs = {}
        attrs['class'] = '%s form-control' % attrs.get('class', '')
        super(EnclosedInput, self).__init__(attrs=attrs)

    def enclose_value(self, value):
        """
        If value doesn't starts with html open sign "<", enclose in add-on tag
        """

        if value.startswith("<button") or value.startswith('<input') and 'type="button"' in value:
            # Surround usign input-group-btb in this case so maintains one line
            value = '<div class="input-group-btn">{0}</div>'.format(value)
            return value
        elif value.startswith('<'):
            return value

        # back support
        if value.startswith("icon-"):
            value = '<span class="glyphicon glyph%s"></span>' % value
        # bs3 syntax
        if value.startswith("glyphicon-"):
            value = '<span class="glyphicon %s"></span>' % value

        return '<span class="input-group-addon">%s</span>' % value


    def render(self, name, value, attrs=None):
        output = super(EnclosedInput, self).render(name, value, attrs)
        if self.prepend:
            self.prepend = self.enclose_value(self.prepend)
            output = ''.join((self.prepend, output))
        if self.append:
            self.append = self.enclose_value(self.append)
            output = ''.join((output, self.append))

        return mark_safe(
            '<div class="input-group form-inline">%s</div>' % output)


class AutosizedTextarea(SuitFormComponentMix, Textarea):
    """
    Autosized Textarea - textarea height dynamically grows based on user input
    """

    def __init__(self, attrs=None):
        new_attrs = _make_attrs(attrs, {"rows": 2}, "autosize")
        super(AutosizedTextarea, self).__init__(new_attrs)

    @property
    def media(self):
        return forms.Media(js=[static("suit/js/jquery.autosize-min.js")])

    def render(self, name, value, attrs=None):
        output = super(AutosizedTextarea, self).render(name, value, attrs)
        output += mark_safe(
            "<script type=\"text/javascript\">Suit.$('#id_%s').autosize();</script>"
            % name)
        return output


#
# Original date widgets with addition html
#
class SuitDateWidget(AdminDateWidget):
    def __init__(self, attrs=None, format=None):
        defaults = {'placeholder': _('Date:')[:-1]}
        new_attrs = _make_attrs(attrs, defaults, "vDateField input-small form-control")
        super(SuitDateWidget, self).__init__(attrs=new_attrs, format=format)

    def render(self, name, value, attrs=None):
        output = super(SuitDateWidget, self).render(name, value, attrs)
        return mark_safe(
            '<div class="input-group suit-date">%s<span '
            # 'class="input-group-addon"><i class="icon-calendar"></i></span></div>' %
            'class="add-on input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span></div>' %
            output)


class SuitTimeWidget(AdminTimeWidget):
    def __init__(self, attrs=None, format=None):
        defaults = {'placeholder': _('Time:')[:-1]}
        new_attrs = _make_attrs(attrs, defaults, "vTimeField input-small form-control")
        super(SuitTimeWidget, self).__init__(attrs=new_attrs, format=format)

    def render(self, name, value, attrs=None):
        output = super(SuitTimeWidget, self).render(name, value, attrs)
        return mark_safe(
            '<div class="input-group suit-date suit-time">%s<span '
            'class="input-group-addon"><span class="glyphicon glyphicon-time"></span></span></div>' %
            output)


class SuitSplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """

    def __init__(self, attrs=None):
        widgets = [SuitDateWidget, SuitTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        out_tpl = '<div class="datetime form-inline">%s %s</div>'
        return mark_safe(out_tpl % (rendered_widgets[0], rendered_widgets[1]))


def _make_attrs(attrs, defaults=None, classes=None):
    result = defaults.copy() if defaults else {}
    if attrs:
        result.update(attrs)
    if classes:
        result["class"] = " ".join((classes, result.get("class", "")))
    return result


class SuitTextInputWidget(SuitFormComponentMix, AdminTextInputWidget):
    pass


class SuitIntegerWidget(SuitFormComponentMix, AdminIntegerFieldWidget):
    pass


class SuitSelectWidget(SuitFormComponentMix, Select):
    pass


class ChoiceFieldRendererBS3(ChoiceFieldRenderer):
    inner_class = {
        CheckboxChoiceInput: 'checkbox'
    }
    # outer_html = '<ul{id_attr}>{content}</ul>'
    outer_html = u'{content}'
    # inner_html = '<li>{choice_value}{sub_widgets}</li>'
    inner_html = u'<div class="%s">{choice_value}{sub_widgets}</div>'

    def __init__(self, name, value, attrs, choices):
        self.inner_html = self.inner_html % self.inner_class.get(self.choice_input_class, '')
        self.name = name
        self.value = value
        self.attrs = attrs
        self.choices = choices


class CheckboxFieldRendererBS3(ChoiceFieldRendererBS3):
    choice_input_class = CheckboxChoiceInput


class SuitCheckboxSelectMultiple(CheckboxSelectMultiple):
    renderer = CheckboxFieldRendererBS3
    _empty_value = []