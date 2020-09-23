#!python3
#-*- coding: utf-8 -*-
"""
    MoreLib Math Module

    This module includes the some simple practical math operations that involve
    usual Python types and are easy to understand and use.

    Functions:
        normalize() -> list[float]: Given a list of numeric natural values, it
            returns its normalization between 0 and 1.
        remap() -> float: Given a value, its original range, and the destiny
            range, it maps it.
        vector_product() -> list[float]: Performs vector operations between
            integer and vectors and vectors with vectors.
        dot_product() -> float: Performs the dot product operation between two
            or more vectors.


    Created:        18 Sep 2020
    Last modified:  18 Sep 2020
        - Ready for version 0.1.0

"""

#
# Functions
#
def normalize (vector):
    """Given a list of numeric natural values, it returns its normalization.

    Raises TypeError exception if the values are not natural numbers.

    """
    if all((isinstance(n, (int, float)) and (n >= 0)) for n in vector):
        out = list()
        for val in vector:
            out.append(val/sum(vector))
        return out
    else:
        raise TypeError("normalize() values must be naturals and >= 0")

def remap (value, *args):
    """Given a numeric `value` within a range and a destiny range, it maps
    the value in the new range.

    You can define the ranges either by writting the minimum and maximum in the
    order (original_min, original_max, destiny_min, destiny_max), or by
    providing two ranges or lists, the first for the origin and the second for
    the destiny.

    Raises ValueError if the ranges are in reversed; or if the value is not
    in the given original range.

    """
    if len(args) == 2:
        omin, *_, omax = list(args[0])
        dmin, *_, dmax = list(args[1])
    elif len(args) == 4:
        omin, omax, dmin, dmax = args

    if (omax <= omin) or (dmax <= dmin):
        raise ValueError("remap() ranges must be from lower to higher")
    if value not in range(omin, omax+1):
        raise ValueError(f"remap() given value '{value}' is not in range "\
                         f"[{omin}, {omax}]")

    r = (value - omin) / (omax - omin)
    ans = dmin + r * (dmax - dmin)
    return ans


def vector_product (v, w, *args):
    """Performs a vector product between two values.

    `w` and `args` must always be lists of numeric values.

    If `v` is an integer, it will multiply it for each value in `w`, returning
    another list. If `args` are provided, it will call itself again with the
    new list as first argument.

    If `v` is a list of values, then all the following lists must have the same
    length, and it will perform a simetrical multiplication, so each index will
    be multiplied and return a new list with the same length.

    Raises ValueError exception if the length or the lists are not equal.

    """
    if isinstance(v, (int, float)):
        # v * [w0 w1 ... wN] operation.
        ans = [v*n for n in w]
        if args:
            return vector_product(ans, *args)
        else:
            return ans
    elif isinstance(v, (list, tuple)):
        # [v0 v1 ... vN] * [w0 w1 ... wN] * ...
        if (len(w) == len(v)) and all(len(x) == len(v) for x in args):
            ans = list()
            for i in range(len(v)):
                n = v[i] * w[i]
                for arg in args:
                    n *= arg[i]
                ans.append(n)
            return ans
        else:
            raise ValueError("vector_product() needs all the lists to have the"\
                             " same length")

def dot_product (v, w, *args):
    """Performs the dot multiplication of two or more lists of numeric values

    Raises ValueError exception if the length of the lists are not equal.

    """
    try:
        vector = vector_product(v, w, *args)
        return sum(vector)
    except ValueError:
        raise ValueError("dot_product() needs all the lists to have the same length")

