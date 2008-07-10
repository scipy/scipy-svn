""" A module for intepolation
"""

#from enthought.interpolate import DataFit, Linear, Block
from interpolate_helper import block, linear, block, Linear, Block, logarithmic
from numpy import array, arange, empty, float64


    

class Interpolate1D(object):
    """ Class for interpolation and extrapolation of functions
        from 1D data.
    
        Parameters
        ----------
        x : array_like
            x values to interpolate from.  Pass in as NumPy array
            or Python list.
        y : array_like
            y values to interpolate from.  Pass in as NumPy array
            or Python list.x and y must be the same length.
        kind : optional
        low : optional
        high : optional

           
        Example
        -------
        # fixme: This should also demonstrate extrapolation.
        
        >>> from numpy import arange, array
        >>> a = arange(10.)
        >>> b = arange(10.) * 2.0
        >>> new_a = array([1.0, 2.5, 8.0, 1.0, -1, 12])
        >>> interp = Interpolate1D(a, b)
        >>> interp(new_a)
        array([  2.,   5.,  16.,   2.,   0.,  18.])

    """
    
    def __init__(self, x, y, kind='Linear', low='Block', high='Block'):
        """ Class constructor
      
        x : array-like
            
        """

        # fixme: Handle checking if they are the correct size.
        self._x = array(x)
        self._y = array(y)
        
        self.kind = self._init_interp_method(x, y, kind)
        self.low = self._init_interp_method(x, y, low)
        self.high = self._init_interp_method(x, y, high)

    def _init_interp_method(self, x, y, kind):
        from inspect import isclass, isfunction
        
        if isinstance(kind, str):
            try:
                exec('from interpolate_helper import %s; kind = %s' % (kind, kind) )
            except:
                raise
        
        if isclass(kind):
            result = kind(x, y)
        elif isfunction(kind):
            result = kind
        else:
            print 'WTF??'
            raise
        return result
    

    def __call__(self, x):
        low_mask = x<self._x[0]
        high_mask = x>self._x[-1]
        interp_mask = (~low_mask) & (~high_mask)
        
        new_interp = self.kind(x[interp_mask])
        new_low = self.low(x[low_mask])
        new_high = self.high(x[high_mask])
                
        # fixme: Handle other data types.                         
        result = empty(x.shape, dtype=float64)
        result[low_mask] = new_low
        result[high_mask] = new_high
        result[interp_mask] = new_interp
        
        return result

if __name__ == '__main__':
    a = arange(10.)
    b = 2*a
    c = array([-1, 4.5, 19])
    interp = Interpolate1D(a, b, kind=lambda x: linear(a,b,x), \
        low='Block', high=lambda x: block(a,b,x) )
    print 'c equals: ', c
    print 'interp(c) equals: ', interp(c)                   