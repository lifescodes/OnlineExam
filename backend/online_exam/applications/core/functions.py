from uuid import uuid4
from django.shortcuts import _get_queryset


def uuid_8_chars():
    return str(uuid4())[:8]


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
