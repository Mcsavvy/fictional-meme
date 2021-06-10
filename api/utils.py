from collections.abc import Iterable
from collections import OrderedDict


def position(integer: int):
    raw = str(integer)
    if integer > 3 and integer < 21:
        return raw + "th"
    elif raw.endswith("1"):
        return raw + "st"
    elif raw.endswith("2"):
        return raw + "nd"
    elif raw.endswith("3"):
        return raw + "rd"
    else:
        return raw + "th"


def pos(integer: int):
    raw = "pos" + str(integer)
    return raw

def prange(Range: int):
    return [pos(i + 1) for i in range(Range)]


def pmap(data: Iterable):
    if not isinstance(data, Iterable):
        return {"pos1": "Data cannot be parsed"}
    od = OrderedDict()
    for i in range(len(data)):
        od[pos(i + 1)] = data[i]
    return od


def _2Dmap(_2Darray):
    mapped = []
    for cols in _2Darray:
        mapped.append(pmap(cols))
    return pmap(mapped)


def _2Darray(data, c, r, spillover=True, fillempty=None):
    reverse_data = data[::-1]
    grid = []
    for col in range(c):
        cols = []
        for row in range(r):
            try:
                cols.append(reverse_data.pop())
            except IndexError:
                if spillover:
                    if fillempty:
                        if isinstance(fillempty, str):
                            debug = fillempty.format(**locals())
                            cols.append(debug)
                        else:
                            cols.append(fillempty)
                    else:
                        grid.append(cols)
                        return grid
        grid.append(cols)
    return grid


def grid(data, xrows=None, ycols=None):
    if not isinstance(data, Iterable):
        return {"pos1": {"1st": "Data cannot be parsed."}}
    if isinstance(data, dict):
        return {"pos1": {"pos1": "Dict object not accepted."}}
    if not any((xrows, ycols)):
        return {"pos1": {"pos1": "No height or width detected."}}
    if all((xrows, ycols)):
        area = (xrows * ycols)
        data = data[:area]
    else:
        if xrows:
            ycols = len(data) // xrows
        elif ycols:
            xrows = len(data) // ycols
    grid = _2Darray(data, ycols, xrows)
    return grid


def gridmap(data, xrows=None, ycols=None):
    grid_ = grid(data, xrows, ycols)
    return _2Dmap(grid_)
