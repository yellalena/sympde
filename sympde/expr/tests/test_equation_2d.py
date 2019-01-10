# coding: utf-8

import pytest

from sympy import Symbol
from sympy.core.containers import Tuple
from sympy import symbols
from sympy import IndexedBase
from sympy import Matrix
from sympy import Function
from sympy import pi, cos, sin
from sympy import srepr
from sympy.physics.quantum import TensorProduct

from sympde.core import Constant
from sympde.core import grad, dot, inner, cross, rot, curl, div
from sympde.core import laplace, hessian, bracket
from sympde.topology import (dx, dy, dz)
from sympde.topology import FunctionSpace, VectorFunctionSpace
from sympde.topology import Field, VectorField
from sympde.topology import ProductSpace
from sympde.topology import TestFunction
from sympde.topology import VectorTestFunction
from sympde.topology import Unknown
from sympde.topology import Domain, Boundary, NormalVector, TangentVector
from sympde.topology import Trace, trace_0, trace_1
from sympde.topology import Square

from sympde.expr import BilinearForm, LinearForm, Integral
from sympde.expr import atomize
from sympde.expr import evaluate
from sympde.expr import tensorize
from sympde.expr import Mass, Stiffness, Advection, AdvectionT
from sympde.expr import Projection
from sympde.expr import Norm
from sympde.expr import FormCall

from sympde.expr.errors import UnconsistentError
from sympde.expr.errors import UnconsistentLhsError
from sympde.expr.errors import UnconsistentRhsError
from sympde.expr.errors import UnconsistentBCError

from sympde.expr import Equation, DirichletBC, EssentialBC

DIM = 2
domain = Domain('Omega', dim=DIM)

#==============================================================================
def test_equation_2d():

    V = FunctionSpace('V', domain)
    U = FunctionSpace('U', domain)

    v = TestFunction(V, name='v')
    u = TestFunction(U, name='u')

    x,y = domain.coordinates

    alpha = Constant('alpha')

    B1 = Boundary(r'\Gamma_1', domain)
    B2 = Boundary(r'\Gamma_2', domain)
    B3 = Boundary(r'\Gamma_3', domain)

    # ... bilinear/linear forms
    expr = dot(grad(v), grad(u))
    a1 = BilinearForm((v,u), expr, name='a1')

    expr = v*u
    a2 = BilinearForm((v,u), expr, name='a2')

    expr = v*trace_0(u, B1)
    a_B1 = BilinearForm((v, u), expr, name='a_B1')

    expr = x*y*v
    l1 = LinearForm(v, expr, name='l1')

    expr = cos(x+y)*v
    l2 = LinearForm(v, expr, name='l2')

    expr = x*y*trace_0(v, B2)
    l_B2 = LinearForm(v, expr, name='l_B2')
    # ...

    # ...
    with pytest.raises(UnconsistentLhsError):
        equation = Equation(a1, l1(v))

    with pytest.raises(UnconsistentLhsError):
        equation = Equation(l1(v), l1(v))

    with pytest.raises(UnconsistentLhsError):
        equation = Equation(a1(v,u) + alpha*a2(v,u), l1(v))
    # ...

    # ...
    with pytest.raises(UnconsistentRhsError):
        equation = Equation(a1(v,u), l1)

    with pytest.raises(UnconsistentRhsError):
        equation = Equation(a1(v,u), a1(v,u))

    with pytest.raises(UnconsistentRhsError):
        equation = Equation(a1(v,u), l1(v) + l2(v))
    # ...

    # ...
    equation = Equation(a1(v,u), l1(v))
    # ...

    # ...
    a = BilinearForm((v,u), a1(v,u) + alpha*a2(v,u))
    equation = Equation(a(v,u), l1(v))
    # ...

    # ...
    a = BilinearForm((v,u), a1(v,u) + a_B1(v,u))
    equation = Equation(a(v,u), l1(v))
    # ...

    # ...
    a = BilinearForm((v,u), a1(v,u) + a_B1(v,u))
    l = LinearForm(v, l1(v) + l2(v))
    equation = Equation(a(v,u), l(v))
    # ...

    # ...
    a = BilinearForm((v,u), a1(v,u) + a_B1(v,u))
    l = LinearForm(v, l1(v) + alpha*l_B2(v))
    equation = Equation(a(v,u), l(v))
    # ...

    # ... using bc
    equation = Equation(a1(v,u), l1(v), bc=DirichletBC(B1))
    # ...

#    # ... using bc
#    equation = Equation(a1(v,u), l1(v), bc=DirichletBC(ComplementBoundary(B1)))
#    # ...

#    # ... TODO FIX THIS, NOT RAISED ANYMORE!
#    with pytest.raises(UnconsistentBCError):
#        a = BilinearForm((v,u), a1(v,u) + a_B1(v,u))
#        equation = Equation(a(v,u), l1(v), bc=DirichletBC(B1))
#    # ...

#    # ... TODO FIX THIS, NOT RAISED ANYMORE!
#    # ...
#    with pytest.raises(UnconsistentBCError):
#        l = LinearForm(v, l1(v) + alpha*l_B2(v))
#        equation = Equation(a1(v,u), l(v), bc=DirichletBC(B2))
#    # ...


#==============================================================================
def test_projection_2d():

    V = FunctionSpace('V', domain)
    x,y = domain.coordinates

    alpha = Constant('alpha')

    u = Projection(x**2+alpha*y, V, name='u')


#==============================================================================
def test_equation_2d_2():

    domain = Square()

    V = FunctionSpace('V', domain)

    x,y = domain.coordinates

    pn = Field('pn', V)
    wn = Field('wn', V)

    dp    = TestFunction(V, name='dp')
    dw    = TestFunction(V, name='dw')
    tau   = TestFunction(V, name='tau')
    sigma = TestFunction(V, name='sigma')

    Re    = Constant('Re', real=True)
    dt    = Constant('dt', real=True)
    alpha = Constant('alpha', real=True)

    s  = BilinearForm((tau,sigma), dot(grad(tau), grad(sigma)))
    m  = BilinearForm((tau,sigma), tau*sigma)
    b1 = BilinearForm((tau,dw), bracket(pn, dw) * tau)
    b2 = BilinearForm((tau,dp), bracket(dp, wn) * tau)

    l1 = LinearForm(tau, bracket(pn, wn)*tau - 1./Re * dot(grad(tau), grad(wn)))

    expr =  m(tau,dw) - alpha*dt*b1(tau,dw) - dt*b2(tau,dp) - (alpha*dt/Re)*s(tau,dw)
    a = BilinearForm(((tau, sigma),(dp,dw)), expr)

    l = LinearForm((tau, sigma), dt*l1(tau))

    equation = Equation(a((tau, sigma),(dp,dw)), l(tau, sigma), bc=DirichletBC(domain.boundary))

    # TODO not working yet!! gives the wrong result => result must be a vector
    # and not a scalar
    print(evaluate(l, verbose=True))
    print(evaluate(equation.rhs.expr, verbose=True))

#==============================================================================
def test_equation_2d_3():

    V = FunctionSpace('V', domain)

    v = TestFunction(V, name='v')
    u = TestFunction(V, name='u')

    x,y = domain.coordinates

    B1 = Boundary(r'\Gamma_1', domain)

    # ... bilinear/linear forms
    a1 = BilinearForm((v,u), dot(grad(v), grad(u)))
    a2 = BilinearForm((v,u), v*u)

    l1 = LinearForm(v, x*y*v)
    l2 = LinearForm(v, cos(x+y)*v)
    # ...

    # ...
    bc = EssentialBC(u, 0, B1)
    eq = Equation(a1(v,u), l1(v), bc=bc)
    # ...

    # ...
    bc = EssentialBC(trace_1(grad(u), B1), 0, B1)
    eq = Equation(a1(v,u), l1(v), bc=bc)
    # ...

#==============================================================================
# CLEAN UP SYMPY NAMESPACE
#==============================================================================

def teardown_module():
    from sympy import cache
    cache.clear_cache()

def teardown_function():
    from sympy import cache
    cache.clear_cache()

test_equation_2d_3()
