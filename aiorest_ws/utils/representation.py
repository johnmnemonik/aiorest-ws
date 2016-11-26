# -*- coding: utf-8 -*-
"""
Helper functions for creating user-friendly representations of serializer
classes and serializer fields.
"""
import re
from aiorest_ws.utils.encoding import force_text

__all__ = ('smart_repr', 'field_repr', 'serializer_repr', 'list_repr')


def smart_repr(value):
    # Convert any type of data to a string
    value = force_text(value)

    # Representations like
    # <django.core.validators.RegexValidator object at 0x1047af050>
    # Should be presented as
    # <django.core.validators.RegexValidator object>
    value = re.sub(' at 0x[0-9A-Fa-f]{4,32}>', '>', value)
    return value


def field_repr(field, force_many=False):
    kwargs = field._kwargs
    if force_many:
        kwargs = kwargs.copy()
        kwargs['many'] = True
        kwargs.pop('child', None)

    arg_string = ', '.join([smart_repr(val) for val in field._args])
    kwarg_string = ', '.join([
        '%s=%s' % (key, smart_repr(val))
        for key, val in sorted(kwargs.items())
    ])
    if arg_string and kwarg_string:
        arg_string += ', '

    if force_many:
        class_name = force_many.__class__.__name__
    else:
        class_name = field.__class__.__name__

    return "%s(%s%s)" % (class_name, arg_string, kwarg_string)


def serializer_repr(serializer, indent, force_many=None):
    ret = field_repr(serializer, force_many) + ':'
    indent_str = '    ' * indent

    if force_many:
        fields = force_many.fields
    else:
        fields = serializer.fields

    for field_name, field in fields.items():
        ret += '\n' + indent_str + field_name + ' = '
        if hasattr(field, 'fields'):
            ret += serializer_repr(field, indent + 1)
        elif hasattr(field, 'child'):
            ret += list_repr(field, indent + 1)
        elif hasattr(field, 'child_relation'):
            ret += field_repr(field.child_relation, force_many=field.child_relation)  # NOQA
        else:
            ret += field_repr(field)

    if serializer.validators:
        ret += '\n' + indent_str + 'class Meta:'
        ret += '\n' + indent_str + '    validators = ' + smart_repr(serializer.validators)  # NOQA

    return ret


def list_repr(serializer, indent):
    child = serializer.child
    if hasattr(child, 'fields'):
        return serializer_repr(serializer, indent, force_many=child)
    return field_repr(serializer)
