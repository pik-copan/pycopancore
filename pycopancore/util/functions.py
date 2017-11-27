import math as ma
import numpy as np
import sympy as sp


def safe_sqrt(x):
    """square root extended to negative values
    
    returns the sign times the sqrt of the abs
    """
    return (sp.sign(x) * sp.sqrt(sp.Abs(x)) if isinstance(x, sp.Expr)
            else np.sign(x) * np.sqrt(np.abs(x)))


def safe_pow(x, e, i=np.inf):
    """modified power function defined for all x and e
    
    returns the sign of x times the abs of x raised to the power e,
    returns i (default:inf) if x == 0 > e
    """
    return (sp.Piecewise(
                (i, x == 0 > e),
                (sp.sign(x) * sp.Pow(sp.Abs(x), e), True))
            if isinstance(x, sp.Expr)
            else i if x == 0 > e
            else np.sign(x) * np.abs(x)**e)


def safe_div(a, b, i=np.inf, z=0):
    """division extended to divisor zero
    
    returns a/b if b!=0, i (default:inf) if b=0<a, -i if b=0>a, 
    and z (default:0) if b=0=a
    """
    return (sp.Piecewise(
                (sp.sign(a) * i, b == 0 != a),
                (z, b == 0),
                (a / b, True))
            if isinstance(a, sp.Expr) or isinstance(b, sp.Expr)
            else np.sign(a) * i if b == 0 != a
            else z if b == 0
            else a / b)


def safe_log(x, i=-np.inf):
    """log extended to all real numbers
    
    returns i (default: -inf) for x <= 0
    """
    return (sp.Piecewise(
                (sp.log(x), x > 0),
                (i, True))
            if isinstance(x, sp.Expr)
            else np.log(x) if x > 0
            else i)
