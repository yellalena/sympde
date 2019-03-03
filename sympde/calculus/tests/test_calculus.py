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
from sympy import expand
from sympy.physics.quantum import TensorProduct

from sympde.core import Constant
from sympde.calculus import grad, dot, inner, cross, rot, curl, div
from sympde.calculus import laplace, hessian, bracket, convect, D
from sympde.calculus import ArgumentTypeError
from sympde.topology import Domain
from sympde.topology import FunctionSpace, VectorFunctionSpace
from sympde.topology import ProductSpace
from sympde.topology import H1Space, HcurlSpace, HdivSpace, L2Space, UndefinedSpace
from sympde.topology import TestFunction, ScalarTestFunction, VectorTestFunction
from sympde.topology import ScalarField, VectorField



#==============================================================================
def test_calculus_2d_1():
    domain = Domain('Omega', dim=2)

    V = FunctionSpace('V', domain)
    W = VectorFunctionSpace('W', domain)

    alpha, beta, gamma = [Constant(i) for i in ['alpha','beta','gamma']]

    f,g,h = [ScalarField(V, name=i) for i in ['f','g','h']]
    F,G,H = [VectorField(W, i) for i in ['F','G','H']]

    # ... scalar gradient properties
    assert( grad(f+g) == grad(f) + grad(g) )
    assert( grad(alpha*f) == alpha*grad(f) )
    assert( grad(alpha*f + beta*g) == alpha*grad(f) + beta*grad(g)  )

    assert( grad(f*g) == f*grad(g) + g*grad(f) )
    assert( grad(f/g) == -f*grad(g)/g**2 + grad(f)/g )

    assert( expand(grad(f*g*h)) == f*g*grad(h) + f*h*grad(g) + g*h*grad(f) )
    # ...

    # ... vector gradient properties
    assert( grad(F+G) == grad(F) + grad(G) )
    assert( grad(alpha*F) == alpha*grad(F) )
    assert( grad(alpha*F + beta*G) == alpha*grad(F) + beta*grad(G)  )

    assert( grad(dot(F,G)) == convect(F, G) + convect(G, F) + cross(F, curl(G)) - cross(curl(F), G) )
    # ...

    # ... curl properties
    assert( curl(f+g) == curl(f) + curl(g) )
    assert( curl(alpha*f) == alpha*curl(f) )
    assert( curl(alpha*f + beta*g) == alpha*curl(f) + beta*curl(g)  )
    # ...

    # ... laplace properties
    assert( laplace(f+g) == laplace(f) + laplace(g) )
    assert( laplace(alpha*f) == alpha*laplace(f) )
    assert( laplace(alpha*f + beta*g) == alpha*laplace(f) + beta*laplace(g)  )
    # ...

    # ... divergence properties
    assert( div(F+G) == div(F) + div(G) )
    assert( div(alpha*F) == alpha*div(F) )
    assert( div(alpha*F + beta*G) == alpha*div(F) + beta*div(G)  )

    assert( div(cross(F,G)) == -dot(F, curl(G)) + dot(G, curl(F)) )
    # ...

    # ... rot properties
    assert( rot(F+G) == rot(F) + rot(G) )
    assert( rot(alpha*F) == alpha*rot(F) )
    assert( rot(alpha*F + beta*G) == alpha*rot(F) + beta*rot(G)  )
    # ...

    expr = grad(dot(F,G))
    print(expr)

#==============================================================================
def test_calculus_2d_2():
    domain = Domain('Omega', dim=2)

    V = FunctionSpace('V', domain)
    W = VectorFunctionSpace('W', domain)

    alpha, beta, gamma = [Constant(i) for i in ['alpha','beta','gamma']]

    f,g,h = [ScalarField(V, name=i) for i in ['f','g','h']]
    F,G,H = [VectorField(W, i) for i in ['F','G','H']]

    # ... vector gradient properties
    assert( convect(F+G, H) == convect(F,H) + convect(G,H) )
    assert( convect(alpha*F,H) == alpha*convect(F,H) )
    assert( convect(F,alpha*H) == alpha*convect(F,H) )
    # ...

#==============================================================================
def test_calculus_3d():
    domain = Domain('Omega', dim=3)

    V = FunctionSpace('V', domain)
    W = VectorFunctionSpace('W', domain)

    alpha, beta, gamma = [Constant(i) for i in ['alpha','beta','gamma']]

    f,g,h = [ScalarField(V, name=i) for i in ['f','g','h']]
    F,G,H = [VectorField(W, i) for i in ['F','G','H']]

    # ... gradient properties
    assert( grad(f+g) == grad(f) + grad(g) )
    assert( grad(alpha*f) == alpha*grad(f) )
    assert( grad(alpha*f + beta*g) == alpha*grad(f) + beta*grad(g)  )

    assert( grad(f*g) == f*grad(g) + g*grad(f) )
    assert( grad(f/g) == -f*grad(g)/g**2 + grad(f)/g )

    assert( expand(grad(f*g*h)) == f*g*grad(h) + f*h*grad(g) + g*h*grad(f) )
    # ...

    # ... curl properties
    assert( curl(F+G) == curl(F) + curl(G) )
    assert( curl(alpha*F) == alpha*curl(F) )
    assert( curl(alpha*F + beta*G) == alpha*curl(F) + beta*curl(G)  )

    assert( curl(cross(F,G)) == F*div(G) - G*div(F) - convect(F, G) + convect(G, F) )
    assert( curl(f*F) == f*curl(F) + cross(grad(f), F) )
    # ...

    # ... laplace properties
    assert( laplace(f+g) == laplace(f) + laplace(g) )
    assert( laplace(alpha*f) == alpha*laplace(f) )
    assert( laplace(alpha*f + beta*g) == alpha*laplace(f) + beta*laplace(g)  )
    assert( laplace(f*g) == f*laplace(g) + g*laplace(f) + 2*dot(grad(f), grad(g)) )
    # ...

    # ... divergence properties
    assert( div(F+G) == div(F) + div(G) )
    assert( div(alpha*F) == alpha*div(F) )
    assert( div(alpha*F + beta*G) == alpha*div(F) + beta*div(G)  )

    assert( div(cross(F,G)) == -dot(F, curl(G)) + dot(G, curl(F)) )
    assert( div(f*F) == f*div(F) + dot(F, grad(f)))
    # ...

    # ...
    assert( curl(grad(f)) == 0 )
    assert( div(curl(F)) == 0 )
    assert( div(cross(grad(f), grad(g))) == 0 )
    assert( curl(curl(F)) == grad(div(F)) - laplace(F))
    assert( curl(f*grad(g)) == cross(grad(f), grad(g)) )
    # ...


#==============================================================================
def test_calculus_3d_3():
    domain = Domain('Omega', dim=3)

    H1    =       FunctionSpace('V0', domain, kind='H1')
    Hcurl = VectorFunctionSpace('V1', domain, kind='Hcurl')
    Hdiv  = VectorFunctionSpace('V2', domain, kind='Hdiv')
    L2    =       FunctionSpace('V3', domain, kind='L2')
    V     =       FunctionSpace('V', domain, kind=None)
    W     = VectorFunctionSpace('W', domain, kind=None)

    f,g,h = [ScalarField(V, name=i) for i in ['f','g','h']]
    F,G,H = [VectorField(W, i) for i in ['F','G','H']]

    X = ProductSpace(H1, Hcurl, Hdiv, L2)
    v0, v1, v2, v3 = TestFunction(X, ['v0', 'v1', 'v2', 'v3'])

    v = TestFunction(V, 'v')
    w = TestFunction(W, 'w')

    # ... consistency of grad operator
    # we can apply grad on an undefined space type or H1
    expr = grad(v0)
    expr = grad(v)
    expr = grad(w)

    # wa cannot apply grad to a function in Hcurl
    with pytest.raises(ArgumentTypeError): expr = grad(v1)

    # wa cannot apply grad to a function in Hdiv
    with pytest.raises(ArgumentTypeError): expr = grad(v2)

    # wa cannot apply grad to a function in L2
    with pytest.raises(ArgumentTypeError): expr = grad(v3)
    # ...

    # ... consistency of curl operator
    # we can apply curl on an undefined space type, H1 or Hcurl
    expr = curl(v0)
    expr = curl(v1)
    expr = curl(v)
    expr = curl(w)

    # wa cannot apply curl to a function in Hdiv
    with pytest.raises(ArgumentTypeError): expr = curl(v2)

    # wa cannot apply curl to a function in L2
    with pytest.raises(ArgumentTypeError): expr = curl(v3)
    # ...

    # ... consistency of div operator
    # we can apply div on an undefined space type, H1 or Hdiv
    expr = div(v0)
    expr = div(v2)
    expr = div(v)
    expr = div(w)

    # wa cannot apply div to a function in Hcurl
    with pytest.raises(ArgumentTypeError): expr = div(v1)

    # wa cannot apply div to a function in L2
    with pytest.raises(ArgumentTypeError): expr = div(v3)
    # ...

#==============================================================================
def test_calculus_3d_4():
    domain = Domain('Omega', dim=3)

    W = VectorFunctionSpace('W', domain)

    alpha, beta, gamma = [Constant(i) for i in ['alpha','beta','gamma']]

    F,G,H = [VectorField(W, i) for i in ['F','G','H']]

    # ...
    expr = inner(D(F), D(G))
    print(expr)
    # ...

    # ...
    expected = alpha*inner(D(F), D(G)) + beta*inner(D(F), D(H))
    assert(inner(D(F), D(alpha*G+beta*H)) == expected)
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

#test_calculus_2d_1()
#test_calculus_2d_2()
#test_calculus_3d()

#test_calculus_3d_3()
#test_calculus_3d_4()
