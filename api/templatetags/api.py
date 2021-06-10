from django import template
from globals.utils import (
    position, prange, grid as Grid
)

register = template.Library()
new = register.filter


def arg_parser(arguments):
    """
    TRIES TO PARSE BOTH KEYWORD AND POSITIONAL ARGUMENTS
    WITH THE && SEPERATOR
    sample positional only arguments;
            'foo&&bar&&baq'
    sample keyword only arguments;
            '??foo=True&&bar=False&&baq=None'
    sample *args and **kwargs;
            'foo&&bar??baq=True'
    """
    arguments = arguments.split("??")
    has_kwargs = True if len(arguments) > 1 else False
    args = []
    for x in arguments[0].split("&&"):
        try:
            args.append(eval(x))
        except Exception:
            args.append(x)
    if has_kwargs:
        kwargs = {}
        for x in arguments[1].split("&&"):
            _ = x.split("=")
            try:
                kwargs[_[0]] = eval(_[1])
            except Exception:
                kwargs[_[0]] = _[1]
    else:
        kwargs = {}
    return args, kwargs


@new()
def to_string(obj):
    return str(object)


@new("grid")
def grid(data, arguments):
    parsed = arg_parser(arguments)
    return Grid(data, *parsed[0], **parsed[1])
