""" helper_funcs.py
"""

import numpy
import _interpolate
print "this is the module"

def make_array_safe(ary, typecode):
    ary = numpy.atleast_1d(numpy.asarray(ary, typecode))
    if not ary.flags['CONTIGUOUS']:
        ary = ary.copy()
    return ary


class Block():
    """ Used when only one element is available in the log.
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    def __call__(self, new_x):
        # find index of values in x that preceed values in x
        # This code is a little strange -- we really want a routine that
        # returns the index of values where x[j] < x[index]
        TINY = 1e-10
        indices = numpy.searchsorted(new_x, new_x+TINY)-1
        
        # If the value is at the front of the list, it'll have -1.
        # In this case, we will use the first (0), element in the array.
        # take requires the index array to be an Int
        indices = numpy.atleast_1d(numpy.clip(indices, 0, numpy.Inf).astype(numpy.int))
        result = numpy.take(self._y, indices, axis=-1)
        return result

class Linear():
    """ Linearly interpolates values in new_x based on the values in x and y

        Parameters
        ----------
        x
            1-D array
        y
            1-D or 2-D array
        new_x
            1-D array
    """
    def __init__(self, x, y):
        self._x = make_array_safe(x, numpy.float64)
        self._y = make_array_safe(y, numpy.float64)

        assert len(y.shape) < 3, "function only works with 1D or 2D arrays"
        
    def __call__(self, new_x):
        new_x = make_array_safe(new_x, numpy.float64)
        if len(self._y.shape) == 2:
            new_y = numpy.zeros((y.shape[0], len(new_x)), numpy.float64)
            for i in range(len(new_y)):
                _interpolate.linear_dddd(x, y[i], new_x, new_y[i])
        else:
            new_y = numpy.zeros(len(new_x), numpy.float64)
            _interpolate.linear_dddd(x, y, new_x, new_y)
        return new_y

def block(x, y, new_x):
    """ Used when only one element is available in the log.
    """

    # find index of values in x that preceed values in x
    # This code is a little strange -- we really want a routine that
    # returns the index of values where x[j] < x[index]
    TINY = 1e-10
    indices = numpy.searchsorted(new_x, new_x+TINY)-1
    
    # If the value is at the front of the list, it'll have -1.
    # In this case, we will use the first (0), element in the array.
    # take requires the index array to be an Int
    indices = numpy.atleast_1d(numpy.clip(indices, 0, numpy.Inf).astype(numpy.int))
    result = numpy.take(y, indices, axis=-1)
    return result
    
def linear(x, y, new_x):
    """ Linearly interpolates values in new_x based on the values in x and y

        Parameters
        ----------
        x
            1-D array
        y
            1-D or 2-D array
        new_x
            1-D array
    """
    x = make_array_safe(x, numpy.float64)
    y = make_array_safe(y, numpy.float64)
    new_x = make_array_safe(new_x, numpy.float64)

    assert len(y.shape) < 3, "function only works with 1D or 2D arrays"
    if len(y.shape) == 2:
        new_y = numpy.zeros((y.shape[0], len(new_x)), numpy.float64)
        for i in range(len(new_y)):
            _interpolate.linear_dddd(x, y[i], new_x, new_y[i])
    else:
        new_y = numpy.zeros(len(new_x), numpy.float64)
        _interpolate.linear_dddd(x, y, new_x, new_y)

    return new_y

class Logarithmic:
    """ For log-linear interpolation
    """
    
    def __init__(self, x, y):
        self._x = make_array_safe(x, numpy.float64)
        self._y = make_array_safe(y, numpy.float64)
        
    def __call__(new_x):
        new_x = make_array_safe(new_x, numpy.float64)
        assert len(y.shape) < 3, "function only works with 1D or 2D arrays"
        if len(y.shape) == 2:
            new_y = numpy.zeros((y.shape[0], len(new_x)), numpy.float64)
            for i in range(len(new_y)):
                _interpolate.loginterp_dddd(x, y[i], new_x, new_y[i])
        else:
            new_y = numpy.zeros(len(new_x), numpy.float64)
            _interpolate.loginterp_dddd(x, y, new_x, new_y)

        return new_y

def logarithmic(x, y, new_x):
    """ Linearly interpolates values in new_x based in the log space of y.

        Parameters
        ----------
        x
            1-D array
        y
            1-D or 2-D array
        new_x
            1-D array
    """
    x = make_array_safe(x, numpy.float64)
    y = make_array_safe(y, numpy.float64)
    new_x = make_array_safe(new_x, numpy.float64)

    assert len(y.shape) < 3, "function only works with 1D or 2D arrays"
    if len(y.shape) == 2:
        new_y = numpy.zeros((y.shape[0], len(new_x)), numpy.float64)
        for i in range(len(new_y)):
            _interpolate.loginterp_dddd(x, y[i], new_x, new_y[i])
    else:
        new_y = numpy.zeros(len(new_x), numpy.float64)
        _interpolate.loginterp_dddd(x, y, new_x, new_y)

    return new_y
    
