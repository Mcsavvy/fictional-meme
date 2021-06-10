from collections.abc import Iterable
from collections import OrderedDict
import sys
import traceback
import random


class Attr:
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return str(self.obj)

    def __str__(self):
        return self.__repr__()

    def __getattr__(self, name):
        if name not in self.__dict__:
            return getattr(self.obj, name, Attr(name))
        return self.__dict__[name]

    def __len__(self):
        return len(self.obj)

    def __bool__(self):
        return bool(self.obj)

    def __iter__(self):
        return iter(self.obj)

    def __call__(self, *_, **__):
        return


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
        return {"pos1": Attr("Data cannot be parsed")}
    od = OrderedDict()
    for i in range(len(data)):
        od[pos(i + 1)] = data[i]
    return od


def _2Dmap(_2Darray):
    mapped = []
    for cols in _2Darray:
        mapped.append(pmap(cols))
    return pmap(mapped)


def _2Darray(data, c, r, spillover=True, fillempty=None, loop=True):
    reverse_data = data[::-1]
    grid = []
    for col in range(c):
        cols = Attr([])
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
    for index, col in enumerate(grid):
        try:
            col.this = index
            col.slide = index + 1
            col.next = grid[index + 1]
        except IndexError:
            if loop:
                try:
                    col.next = grid[0]
                except IndexError:
                    col.next = None
            else:
                col.next = None
        col.parent = grid
    return grid


def grid(
    data, xrows=None, ycols=None, *,
    shuffle=False, slide=0, loop=True,
    spillover=False, fillempty=""
):
    if not isinstance(data, Iterable):
        return [[Attr("Data cannot be parsed.")]]
    data = list(data)
    if isinstance(data, dict):
        return [[Attr("Dict object not accepted.")]]
    if not any((xrows, ycols)):
        return [[Attr("No height or width detected.")]]
    if all((xrows, ycols)):
        area = (xrows * ycols)
        data = data[:area]
    else:
        if xrows:
            ycols = len(data) // xrows
        elif ycols:
            xrows = len(data) // ycols
    grid = _2Darray(
        data, ycols, xrows,
        loop=loop, fillempty=fillempty,
        spillover=spillover
    )
    if shuffle:
        random.shuffle(grid)
    try:
        return grid[(slide % len(grid)) - 1] if slide else grid
    except ZeroDivisionError:
        return grid


def gridmap(data, xrows=None, ycols=None):
    grid_ = grid(data, xrows, ycols)
    return _2Dmap(grid_)



