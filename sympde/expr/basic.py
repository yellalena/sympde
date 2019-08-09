# coding: utf-8

from itertools import groupby

from sympy.core import Basic
from sympy.core import Symbol
from sympy.core import Function
from sympy.simplify.simplify import simplify
from sympy import collect
from sympy.series.order import Order
from sympy.core import Expr, Add, Mul, Pow
from sympy import S
from sympy.core.containers import Tuple
from sympy import Indexed, IndexedBase, Matrix, ImmutableDenseMatrix
from sympy import expand
from sympy import Integer, Float
from sympy.core.expr import AtomicExpr
from sympy.physics.quantum import TensorProduct
from sympy.series.series import series
from sympy.core.compatibility import is_sequence

from sympde.core.basic import _coeffs_registery
from sympde.core.basic import CalculusFunction
from sympde.core.basic import Constant
from sympde.core.algebra import (Dot_1d,
                 Dot_2d, Inner_2d, Cross_2d,
                 Dot_3d, Inner_3d, Cross_3d)
from sympde.core.utils import random_string

from sympde.calculus import Dot, Inner, Cross
from sympde.calculus import Grad, Rot, Curl, Div
from sympde.calculus import Bracket
from sympde.calculus import Laplace
from sympde.calculus.core import _generic_ops

from sympde.topology import BasicDomain, Domain, MappedDomain, Union, Interval
from sympde.topology import BoundaryVector, NormalVector, TangentVector, Boundary
from sympde.topology.derivatives import _partial_derivatives
from sympde.topology.derivatives import partial_derivative_as_symbol
from sympde.topology.derivatives import sort_partial_derivatives
from sympde.topology.derivatives import get_atom_derivatives
from sympde.topology.derivatives import dx, dy, dz
from sympde.topology.derivatives import (Grad_1d, Div_1d,
                                         Grad_2d, Curl_2d, Rot_2d, Div_2d,
                                         Grad_3d, Curl_3d, Div_3d)
from sympde.topology.derivatives import Bracket_2d
from sympde.topology.derivatives import Laplace_1d, Laplace_2d, Laplace_3d
from sympde.topology.derivatives import Hessian_1d, Hessian_2d, Hessian_3d
from sympde.topology.space import BasicFunctionSpace
from sympde.topology.space import ScalarFunctionSpace
from sympde.topology.space import ProductSpace
from sympde.topology.space import ScalarTestFunction
from sympde.topology.space import VectorTestFunction
from sympde.topology.space import Element
from sympde.topology.space import IndexedTestTrial
from sympde.topology.space import Unknown, VectorUnknown
from sympde.topology.space import Trace
from sympde.topology.space import ScalarField, VectorField, IndexedVectorField
from sympde.topology.space import Element, IndexedElement
from sympde.topology.measure import CanonicalMeasure
from sympde.topology.measure import CartesianMeasure
from sympde.topology.measure import Measure



#==============================================================================
def _sanitize_arguments(arguments, is_bilinear=False, is_linear=False):

    # ...
    if is_bilinear or is_linear:

        if is_bilinear:
            test_functions = arguments[0]

        elif is_linear:
            test_functions = arguments

        if isinstance(test_functions, (ScalarTestFunction, VectorTestFunction, Element)):
            test_functions = [test_functions]

        elif isinstance(test_functions, (tuple, list, Tuple)):
            are_valid = [isinstance(i, (ScalarTestFunction, VectorTestFunction, Element)) for i in test_functions]
            if not all(are_valid):
                raise TypeError('> Wrong arguments for test functions')

        else:
            msg = 'Wrong type for test function(s). given {}'.format(type(test_functions))
            raise TypeError(msg)

        test_functions = Tuple(*test_functions)
    # ...

    # ...
    if is_bilinear:

        trial_functions = arguments[1]
        if isinstance(trial_functions, (ScalarTestFunction, VectorTestFunction, Element)):
            trial_functions = [trial_functions]

        elif isinstance(trial_functions, (tuple, list, Tuple)):
            are_valid = [isinstance(i, (ScalarTestFunction, VectorTestFunction, Element)) for i in trial_functions]
            if not all(are_valid):
                raise TypeError('> Wrong arguments for trial functions')

        else:
            msg = 'Wrong type for trial function(s). given {}'.format(type(trial_functions))
            raise TypeError(msg)

        trial_functions = Tuple(*trial_functions)
    # ...

    if is_bilinear:
        args = [test_functions, trial_functions]
        args = Tuple(*args)

    else:
        args = Tuple(*test_functions)

    return args

#==============================================================================
def is_linear_form(expr, args):
    """checks if an expression is linear with respect to the given arguments."""
    # ...
    test_functions = _sanitize_arguments(args, expr, is_linear=True)
    # TODO is it ok to do this?
    test_functions = test_functions[0]

    if isinstance(test_functions, (ScalarTestFunction, VectorTestFunction)):
        test_functions = [test_functions]

    elif isinstance(test_functions, (tuple, list, Tuple)):
        test_functions = list(*test_functions)
    # ...

    # ...
    if not is_linear_expression(expr, test_functions):
        msg = ' Expression is not linear w.r.t [{}]'.format(test_functions)
        raise UnconsistentLinearExpressionError(msg)
    # ...

    return True


#==============================================================================
class BasicExpr(Expr):
    is_Function   = True
    is_linear     = False
    is_bilinear   = False
    is_functional = False

    # TODO use .atoms
    @property
    def fields(self):
        ls = [a for a in self.expr.free_symbols if isinstance(a, (ScalarField, VectorField))]
        # no redanduncy
        return sorted(list(set(ls)))

    # TODO use .atoms
    @property
    def constants(self):
        ls = [a for a in self.expr.free_symbols if isinstance(a, Constant)]
        # no redanduncy
        return list(set(ls))


#==============================================================================
# TODO check unicity of domain in __new__
class BasicForm(Expr):
    is_Function = True
    is_linear   = False
    is_bilinear = False
    is_functional = False
    is_annotated  = False
    is_norm       = False
    _domain     = None
    _ldim        = None
    _body       = None
    _kwargs     = None

    @property
    def fields(self):
        atoms  = self.expr.atoms(Element,ScalarField, VectorField)
        
        if self.is_bilinear or self.is_linear:
            args = self.variables
            if self.is_bilinear:
                args = args[0]+args[1]
            fields = list(atoms.difference(args))
        else:
            fields = list(atoms)
        # no redanduncy
        return fields

    # TODO use .atoms
    @property
    def constants(self):
        ls = [a for a in self.expr.free_symbols if isinstance(a, Constant)]
        # no redanduncy
        return list(set(ls))

    @property
    def domain(self):
        return self._domain

    @property
    def ldim(self):
        return self._ldim

    def get_free_variables(self):
        if self._kwargs is None:
            fields = self.fields
            constants = self.constants

            _kwargs = {}
            for i in fields + constants:
                _kwargs[i.name] = i

            self._kwargs = _kwargs

        return self._kwargs

    def _update_free_variables(self, **kwargs):

        expr = self.expr

        if not kwargs:
            return expr

        # ... use free variables if given and available
        _kwargs = self.get_free_variables()
        _kwargs_names = list(_kwargs.keys())
        for name, v in kwargs.items():
            if not(name in _kwargs_names):
                raise ValueError('{} is not a free variable'.format(name))

            var = _kwargs[name]
            expr = expr.xreplace({var: v})
        # ...

        return expr
        
    def _annotate(self):
    
        if self.is_annotated:
            return self

        if self.is_bilinear:
            test_functions  = self.test_functions
            trial_functions = self.trial_functions
            fields          = self.fields
            new_test_functions  = [f.space.element(f.name) for f in test_functions]
            new_trial_functions = [f.space.element(f.name) for f in trial_functions]
            new_fields          = [f.space.field(f.name) for f in fields]
            expr = self.subs(zip(test_functions, new_test_functions))
            expr = expr.subs(zip(trial_functions, new_trial_functions))
            expr = expr.subs(zip(fields, new_fields))
            
        elif self.is_linear:
            test_functions  = self.test_functions
            fields          = self.fields
            new_test_functions  = [f.space.element(f.name) for f in test_functions]
            new_fields          = [f.space.field(f.name) for f in fields]
            expr = self.subs(zip(test_functions, new_test_functions))
            expr = expr.subs(zip(fields, new_fields))
            
        elif self.is_functional:
            domain = self.domain
            expr   = self.expr
            fields = self.fields
            new_fields = [f.space.field(f.name) for f in fields]
            expr = expr.subs(zip(fields, new_fields))
            expr = self.func(expr, self.domain, eval=False)
            if self.is_norm:
                expr._exponent = self._exponent
            
        else:
            raise NotImplementedError('TODO')
        expr.is_annotated = True
        return expr
