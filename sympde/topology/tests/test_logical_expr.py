# coding: utf-8

from sympy import Symbol, symbols
from sympy import Matrix
from sympy import expand
from sympy import cos, sin, sqrt, pi

from sympde.core     import Constant
from sympde.topology import Domain, Mapping
from sympde.topology import dx, dy
from sympde.topology import dx1, dx2, dx3
from sympde.topology import ScalarFunctionSpace, VectorFunctionSpace
from sympde.topology import element_of, elements_of
from sympde.topology import LogicalExpr
from sympde.topology import SymbolicExpr
from sympde.topology import IdentityMapping
from sympde.topology import PolarMapping
from sympde.topology import TargetMapping
from sympde.topology import CzarnyMapping
from sympde.topology import CollelaMapping
from sympde.topology import TorusMapping
from sympde.topology import TwistedTargetMapping

from sympde.expr     import BilinearForm, integral
from sympde.calculus import grad, div, curl, dot

from sympde.topology.mapping import Jacobian

#==============================================================================
def test_logical_expr_1d_1():
    rdim = 1

    M = Mapping('M', rdim)
    domain = M(Domain('Omega', dim=rdim))

    alpha = Constant('alpha')

    V = ScalarFunctionSpace('V', domain, kind='h1')

    u,v = [element_of(V, name=i) for i in ['u', 'v']]

    det_M = Jacobian(M).det()
    #print('det = ', det_M)
    det   = Symbol('det')

    # ...
    expr = 2*u + alpha*v
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr)
    #print('')
    # ...

    # ...
    expr = dx(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

    # ...
    expr = dx(det_M)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = expr.subs(det_M, det)
    expr = expand(expr)
    #print(expr)
    #print('')
    # ...

    # ...
    expr = dx(dx(u))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

#==============================================================================
def test_symbolic_expr_1d_1():
    rdim = 1

    M = Mapping('M', rdim)
    domain = M(Domain('Omega', dim=rdim))

    alpha = Constant('alpha')

    V = ScalarFunctionSpace('V', domain, kind='h1')

    u = element_of(V, name='u')

    det_M = Jacobian(M).det()
    det_M = SymbolicExpr(det_M)
    #print('>>> ', det_M)
    det   = Symbol('det')

    # ...
    expr = u
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx1(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx1(M[0])
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expr)
    # ...

    # ...
    expr = dx(Jacobian(M).det())
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))
    # ...

    # ...
    expr = dx(dx(u))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))
    # ...

    # ...
    expr = dx(dx(dx(u)))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))
    # ...

#==============================================================================
def test_logical_expr_2d_1():
    rdim = 2

    M = Mapping('M', rdim)
    domain = M(Domain('Omega', dim=rdim))

    alpha = Constant('alpha')

    V = ScalarFunctionSpace('V', domain, kind='h1')
    W = VectorFunctionSpace('V', domain, kind='h1')

    u,v = [element_of(V, name=i) for i in ['u', 'v']]
    w = element_of(W, name='w')

    det_M = Jacobian(M).det()
    #print('det = ', det_M)
    det   = Symbol('det')

    # ...
    expr = 2*u + alpha*v
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr)
    #print('')
    # ...

    # ...
    expr = dx(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

    # ...
    expr = dy(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

    # ...
    expr = dx(det_M)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = expr.subs(det_M, det)
    expr = expand(expr)
    #print(expr)
    #print('')
    # ...

    # ...
    expr = dx(dx(u))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

    # ...
    expr = dx(w[0])
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

#==============================================================================
def test_symbolic_expr_2d_1():
    rdim = 2

    M = Mapping('M', rdim)
    domain = M(Domain('Omega', dim=rdim))

    alpha = Constant('alpha')

    V = ScalarFunctionSpace('V', domain, kind='h1')

    u = element_of(V, name='u')

    det_M = Jacobian(M).det()
    det_M = SymbolicExpr(det_M)
    #print('>>> ', det_M)
    det   = Symbol('det')

    # ...
    expr = u
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx1(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx1(dx2(u))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx1(M[0])
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expr)
    # ...

    # ...
    expr = dx(Jacobian(M).det())
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))
    # ...

    # ...
    expr = dx(dx(u))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))
    # ...

    # ...
    expr = dx(dx(dx(u)))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))
    # ...

#==============================================================================
def test_logical_expr_3d_1():
    rdim = 3

    M = Mapping('M', rdim)
    domain = M(Domain('Omega', dim=rdim))

    alpha = Constant('alpha')

    V = ScalarFunctionSpace('V', domain, kind='h1')

    u,v = [element_of(V, name=i) for i in ['u', 'v']]

    det_M = Jacobian(M).det()
    #print('det = ', det_M)
    det   = Symbol('det')

    # ...
    expr = 2*u + alpha*v
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr)
    #print('')
    # ...

    # ...
    expr = dx(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

    # ...
    expr = dy(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

    # ...
    expr = dx(det_M)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = expr.subs(det_M, det)
    #print(expr)
    #print('')
    # ...

    # ...
    expr = dx(dx(u))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    #print(expr.subs(det_M, det))
    #print('')
    # ...

def test_logical_expr_3d_2():

    dim   = 3
    domain = Domain('Omega', dim=dim)
    M      = Mapping('M', dim=dim)

    mapped_domain = M(domain)

    V  = ScalarFunctionSpace('V' , domain, kind='h1')
    VM = ScalarFunctionSpace('VM', mapped_domain, kind='h1')

    u,v   = elements_of(V, names='u,v')
    um,vm = elements_of(VM, names='u,v')

    J   = M.jacobian

    a = dot(grad(um),grad(vm))
    e = LogicalExpr(a, mapping=M, dim=dim)

    assert e == dot(J.inv().T*grad(u), J.inv().T*grad(v))


def test_logical_expr_3d_3():

    dim    = 3
    domain = Domain('Omega', dim=dim)
    M      = Mapping('M', dim=3)

    mapped_domain = M(domain)

    V  = VectorFunctionSpace('V' , domain, kind='hcurl')
    VM = VectorFunctionSpace('VM', mapped_domain, kind='hcurl')

    u,v   = elements_of(V, names='u,v')
    um,vm = elements_of(VM, names='u,v')

    J   = M.jacobian

    a = dot(curl(um), curl(vm))
    e = LogicalExpr(a, mapping=M, dim=dim)

    assert e == dot(J/J.det()*curl(u), J/J.det()*curl(v))

def test_logical_expr_3d_4():

    dim    = 3
    domain = Domain('Omega', dim=dim)
    M      = Mapping('M', dim=3)

    mapped_domain = M(domain)

    V  = VectorFunctionSpace('V' , domain, kind='hdiv')
    VM = VectorFunctionSpace('VM', mapped_domain, kind='hdiv')

    u,v   = elements_of(V, names='u,v')
    um,vm = elements_of(VM, names='u,v')

    J   = M.jacobian

    a = div(um)*div(vm)
    e = LogicalExpr(a, mapping=M, dim=dim)

    assert e == J.det()**-2*div(u)*div(v)

def test_logical_expr_3d_5():

    dim    = 3
    domain = Domain('Omega', dim=dim)
    M      = Mapping('M', dim=dim)

    mapped_domain = M(domain)

    V  = VectorFunctionSpace('V' , domain, kind='hcurl')
    VM = VectorFunctionSpace('VM', mapped_domain, kind='hcurl')

    J   = M.jacobian
    u,v   = elements_of(V,  names='u,v')
    um,vm = elements_of(VM, names='u,v')

    int_md = lambda expr: integral(mapped_domain , expr)
    int_ld = lambda expr: integral(domain , expr)

    am  = BilinearForm((um,vm), int_md(dot(curl(vm),curl(um))))
    a   = LogicalExpr(am)

    assert a == BilinearForm((u,v), int_ld(sqrt((J.T*J).det())*dot(J/J.det()*curl(u), J/J.det()*curl(v))))



#==============================================================================
def test_symbolic_expr_3d_1():
    rdim = 3

    M = Mapping('M', rdim)
    domain = M(Domain('Omega', dim=rdim))

    alpha = Constant('alpha')

    V = ScalarFunctionSpace('V', domain, kind='h1')
    u = element_of(V, 'u')

    det_M = Jacobian(M).det()
    det_M = SymbolicExpr(det_M)
    #print('>>> ', det_M)
    det   = Symbol('det')

    # ...
    expr = u
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx1(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx1(dx2(u))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx1(M[0])
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    #print(expr)
    # ...

    # ...
    expr = dx(u)
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expr)
    # ...

    # ...
    expr = dx(Jacobian(M).det())
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))
    # ...

    # ...
    expr = dx(dx(u))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))
    # ...

    # ...
    expr = dx(dx(dx(u)))
    expr = LogicalExpr(expr, mapping=M, dim=rdim)
    expr = SymbolicExpr(expr)
    expr = expr.subs(det_M, det)
    #print(expand(expr))

    # ...

#==============================================================================
def test_identity_mapping_2d_1():
    rdim = 2

    x1, x2 = symbols('x1, x2')

    M = IdentityMapping('M', rdim)

    assert(not( M[0] == x1 ))
    assert(not( M[1] == x2 ))

    assert(LogicalExpr(M[0], mapping=M, dim=rdim, subs=True) == x1)
    assert(LogicalExpr(M[1], mapping=M, dim=rdim, subs=True) == x2)

    assert(LogicalExpr(dx1(M[0]), mapping=M, dim=rdim, subs=True) == 1)
    assert(LogicalExpr(dx1(M[1]), mapping=M, dim=rdim, subs=True) == 0)

    assert(LogicalExpr(dx2(M[0]), mapping=M, dim=rdim, subs=True) == 0)
    assert(LogicalExpr(dx2(M[1]), mapping=M, dim=rdim, subs=True) == 1)

    expected = Matrix([[1, 0], [0, 1]])
    assert(not( M.jacobian == expected))
    assert(LogicalExpr(Jacobian(M), mapping=M, dim=rdim, subs=True) == expected)


#==============================================================================
def test_identity_mapping_2d_2():
    rdim = 2

    x1, x2 = symbols('x1, x2')

    M      = IdentityMapping('F', rdim)
    domain = M(Domain('Omega', dim=rdim))


    V = ScalarFunctionSpace('V', domain, kind='h1')
    u = element_of(V, name='u')

    # ...
    assert(LogicalExpr(dx(u), mapping=M, dim=rdim, subs=True) == dx1(u))
    assert(LogicalExpr(dy(u), mapping=M, dim=rdim, subs=True) == dx2(u))
    # ...

#==============================================================================
def test_polar_mapping_2d_1():
    rdim = 2

    x1, x2 = symbols('x1, x2')

    constants = ['c1', 'c2', 'rmax', 'rmin']
    c1, c2, rmax, rmin = [Constant(i) for i in constants]

    M = PolarMapping('M', rdim)

    assert(not( M[0] == x1 ))
    assert(not( M[1] == x2 ))

    assert(LogicalExpr(M[0], mapping=M, dim=rdim, subs=True) == c1 + (rmax*x1 + rmin*(-x1 + 1))*cos(x2))
    assert(LogicalExpr(M[1], mapping=M, dim=rdim, subs=True) == c2 + (rmax*x1 + rmin*(-x1 + 1))*sin(x2))

    assert(LogicalExpr(dx1(M[0]), mapping=M, dim=rdim, subs=True) == (rmax - rmin)*cos(x2))
    assert(LogicalExpr(dx1(M[1]), mapping=M, dim=rdim, subs=True) == (rmax - rmin)*sin(x2))

    expected = -(rmax*x1 + rmin*(-x1 + 1))*sin(x2)
    assert(expand(LogicalExpr(dx2(M[0]), mapping=M, dim=rdim, subs=True)) == expand(expected))
    assert(LogicalExpr(dx2(M[1]), mapping=M, dim=rdim, subs=True) == (rmax*x1 + rmin*(-x1 + 1))*cos(x2))

    expected = Matrix([[(rmax - rmin)*cos(x2), -(rmax*x1 + rmin*(-x1 + 1))*sin(x2)],
                       [(rmax - rmin)*sin(x2), (rmax*x1 + rmin*(-x1 + 1))*cos(x2)]])
    assert(expand(LogicalExpr(Jacobian(M), mapping=M, dim=rdim, subs=True)) == expand(expected))

#==============================================================================
def test_target_mapping_2d_1():
    rdim = 2

    x1, x2 = symbols('x1, x2')

    constants = ['c1', 'c2', 'D', 'k']
    c1, c2, D, k = [Constant(i) for i in constants]

    M = TargetMapping('M', rdim)

    assert(not( M[0] == x1 ))
    assert(not( M[1] == x2 ))

    assert(LogicalExpr(M[0], mapping=M, dim=rdim, subs=True) == -D*x1**2 + c1 + x1*(-k + 1)*cos(x2))
    assert(LogicalExpr(M[1], mapping=M, dim=rdim, subs=True) == c2 + x1*(k + 1)*sin(x2))

    assert(LogicalExpr(dx1(M[0]), mapping=M, dim=rdim, subs=True) == -2*D*x1 + (-k + 1)*cos(x2))
    assert(LogicalExpr(dx1(M[1]), mapping=M, dim=rdim, subs=True) == (k + 1)*sin(x2))

    assert(LogicalExpr(dx2(M[0]), mapping=M, dim=rdim, subs=True) == -x1*(-k + 1)*sin(x2))
    assert(LogicalExpr(dx2(M[1]), mapping=M, dim=rdim, subs=True) == x1*(k + 1)*cos(x2))

    expected = Matrix([[-2*D*x1 + (-k + 1)*cos(x2),
                        -x1*(-k + 1)*sin(x2)],
                       [(k + 1)*sin(x2),
                        x1*(k + 1)*cos(x2)]])

    assert(not( Jacobian(M) == expected))
    assert(expand(LogicalExpr(Jacobian(M), mapping=M, dim=rdim, subs=True)) == expand(expected))

#==============================================================================
def test_czarny_mapping_2d_1():
    rdim = 2

    x1, x2 = symbols('x1, x2')

    constants = ['c2', 'eps', 'b']
    c2, eps, b = [Constant(i) for i in constants]

    M = CzarnyMapping('M', rdim)

    assert(not( M[0] == x1 ))
    assert(not( M[1] == x2 ))

    expected =  (-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 1)/eps
    assert(LogicalExpr(M[0], mapping=M, dim=rdim, subs=True) == expected)
    expected =  b*x1*sin(x2)/(sqrt(-eps**2/4 + 1)*(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2)) + c2
    assert(LogicalExpr(M[1], mapping=M, dim=rdim, subs=True) == expected)

    expected =  -cos(x2)/sqrt(eps*(eps + 2*x1*cos(x2)) + 1)
    assert(LogicalExpr(dx1(M[0]), mapping=M, dim=rdim, subs=True) == expected)
    expected =  b*(eps*x1*sin(x2)*cos(x2)/(sqrt(-eps**2/4 + 1)*sqrt(eps*(eps + 2*x1*cos(x2)) + 1)*(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2)**2) + sin(x2)/(sqrt(-eps**2/4 + 1)*(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2)))
    assert((LogicalExpr(dx1(M[1]), mapping=M, dim=rdim, subs=True) - expected).expand() == 0)

    expected =  x1*sin(x2)/sqrt(eps*(eps + 2*x1*cos(x2)) + 1)
    assert(LogicalExpr(dx2(M[0]), mapping=M, dim=rdim, subs=True) == expected)
    expected =  b*x1*(-eps*x1*sin(x2)**2/(sqrt(eps*(eps + 2*x1*cos(x2)) + 1)*(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2)**2) + cos(x2)/(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2))/sqrt(-eps**2/4 + 1)
    assert((LogicalExpr(dx2(M[1]), mapping=M, dim=rdim, subs=True) - expected).expand() == 0)

    expected =  Matrix([[-cos(x2)/sqrt(eps*(eps + 2*x1*cos(x2)) + 1),
                         x1*sin(x2)/sqrt(eps*(eps + 2*x1*cos(x2)) + 1)],
                        [b*(eps*x1*sin(x2)*cos(x2)/(sqrt(-eps**2/4 + 1)*sqrt(eps*(eps + 2*x1*cos(x2)) + 1)*(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2)**2) + sin(x2)/(sqrt(-eps**2/4 + 1)*(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2))),
                         b*x1*(-eps*x1*sin(x2)**2/(sqrt(eps*(eps + 2*x1*cos(x2)) + 1)*(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2)**2) + cos(x2)/(-sqrt(eps*(eps + 2*x1*cos(x2)) + 1) + 2))/sqrt(-eps**2/4 + 1)]])
    assert(not( Jacobian(M) == expected))
    assert(expand(LogicalExpr(Jacobian(M), mapping=M, dim=rdim, subs=True)) == expand(expected))

#==============================================================================
def test_collela_mapping_2d_1():
    rdim = 2

    x1, x2 = symbols('x1, x2')

    constants = ['eps', 'k1', 'k2']
    eps, k1, k2 = [Constant(i) for i in constants]

    M = CollelaMapping('M', rdim)

    assert(not( M[0] == x1 ))
    assert(not( M[1] == x2 ))

    expected = 2.0*eps*sin(2.0*k1*pi*x1)*sin(2.0*k2*pi*x2) + 2.0*x1 - 1.0
    assert(LogicalExpr(M[0], mapping=M, dim=rdim, subs=True) == expected)
    expected = 2.0*eps*sin(2.0*k1*pi*x1)*sin(2.0*k2*pi*x2) + 2.0*x2 - 1.0
    assert(LogicalExpr(M[1], mapping=M, dim=rdim, subs=True) == expected)

    expected = 4.0*eps*k1*pi*sin(2.0*k2*pi*x2)*cos(2.0*k1*pi*x1) + 2.0
    assert(LogicalExpr(dx1(M[0]), mapping=M, dim=rdim, subs=True) == expected)
    expected = 4.0*eps*k1*pi*sin(2.0*k2*pi*x2)*cos(2.0*k1*pi*x1)
    assert(LogicalExpr(dx1(M[1]), mapping=M, dim=rdim, subs=True) == expected)

    expected = 4.0*eps*k2*pi*sin(2.0*k1*pi*x1)*cos(2.0*k2*pi*x2)
    assert(LogicalExpr(dx2(M[0]), mapping=M, dim=rdim, subs=True) == expected)
    expected = 4.0*eps*k2*pi*sin(2.0*k1*pi*x1)*cos(2.0*k2*pi*x2) + 2.0
    assert(LogicalExpr(dx2(M[1]), mapping=M, dim=rdim, subs=True) == expected)

    expected = Matrix([[4.0*eps*k1*pi*sin(2.0*k2*pi*x2)*cos(2.0*k1*pi*x1) + 2.0,
                        4.0*eps*k2*pi*sin(2.0*k1*pi*x1)*cos(2.0*k2*pi*x2)],
                       [4.0*eps*k1*pi*sin(2.0*k2*pi*x2)*cos(2.0*k1*pi*x1),
                        4.0*eps*k2*pi*sin(2.0*k1*pi*x1)*cos(2.0*k2*pi*x2) + 2.0]])
    assert(not( Jacobian(M) == expected))
    assert(expand(LogicalExpr(Jacobian(M), mapping=M, dim=rdim, subs=True)) == expand(expected))

#==============================================================================
def test_torus_mapping_3d_1():
    rdim = 3

    x1, x2, x3 = symbols('x1, x2, x3')
    R0 = Constant('R0')

    M = TorusMapping('M', rdim)

    assert(not( M[0] == x1 ))
    assert(not( M[1] == x2 ))
    assert(not( M[2] == x3 ))

    expected = (R0 + x1*cos(x2))*cos(x3)
    assert(LogicalExpr(M[0], mapping=M, dim=rdim, subs=True) == expected)
    expected = (R0 + x1*cos(x2))*sin(x3)
    assert(LogicalExpr(M[1], mapping=M, dim=rdim, subs=True) == expected)
    expected = x1*sin(x2)
    assert(LogicalExpr(M[2], mapping=M, dim=rdim, subs=True) == expected)

    expected = cos(x2)*cos(x3)
    assert(LogicalExpr(dx1(M[0]), mapping=M, dim=rdim, subs=True) == expected)
    expected = sin(x3)*cos(x2)
    assert(LogicalExpr(dx1(M[1]), mapping=M, dim=rdim, subs=True) == expected)
    expected = sin(x2)
    assert(LogicalExpr(dx1(M[2]), mapping=M, dim=rdim, subs=True) == expected)

    expected = -x1*sin(x2)*cos(x3)
    assert(LogicalExpr(dx2(M[0]), mapping=M, dim=rdim, subs=True) == expected)
    expected = -x1*sin(x2)*sin(x3)
    assert(LogicalExpr(dx2(M[1]), mapping=M, dim=rdim, subs=True) == expected)
    expected = x1*cos(x2)
    assert(LogicalExpr(dx2(M[2]), mapping=M, dim=rdim, subs=True) == expected)

    expected = -(R0 + x1*cos(x2))*sin(x3)
    assert(expand(LogicalExpr(dx3(M[0]), mapping=M, dim=rdim, subs=True)) == expand(expected))
    expected = (R0 + x1*cos(x2))*cos(x3)
    assert(LogicalExpr(dx3(M[1]), mapping=M, dim=rdim, subs=True) == expected)
    expected = 0
    assert(LogicalExpr(dx3(M[2]), mapping=M, dim=rdim, subs=True) == expected)

    expected = Matrix([[cos(x2)*cos(x3),-x1*sin(x2)*cos(x3),-(R0+x1*cos(x2))*sin(x3)],
                       [sin(x3)*cos(x2),-x1*sin(x2)*sin(x3),(R0+x1*cos(x2))*cos(x3)],
                       [sin(x2), x1*cos(x2), 0]])
    assert(not( Jacobian(M) == expected))
    assert(expand(LogicalExpr(Jacobian(M), mapping=M, dim=rdim, subs=True)) == expand(expected))

#==============================================================================
def test_twisted_target_mapping_3d_1():
    rdim = 3

    x1, x2, x3 = symbols('x1, x2, x3')

    constants = ['c1', 'c2', 'c3', 'D', 'k']
    c1, c2, c3, D, k = [Constant(i) for i in constants]

    M = TwistedTargetMapping('M', rdim)

    assert(not( M[0] == x1 ))
    assert(not( M[1] == x2 ))
    assert(not( M[2] == x3 ))

    expected = -D*x1**2 + c1 + x1*(-k + 1)*cos(x2)
    assert(LogicalExpr(M[0], mapping=M, dim=rdim, subs=True) == expected)
    expected = c2 + x1*(k + 1)*sin(x2)
    assert(LogicalExpr(M[1], mapping=M, dim=rdim, subs=True) == expected)
    expected = c3 + x1**2*x3*sin(2*x2)
    assert(LogicalExpr(M[2], mapping=M, dim=rdim, subs=True) == expected)

    expected = -2*D*x1 + (-k + 1)*cos(x2)
    assert(LogicalExpr(dx1(M[0]), mapping=M, dim=rdim, subs=True) == expected)
    expected = (k + 1)*sin(x2)
    assert(LogicalExpr(dx1(M[1]), mapping=M, dim=rdim, subs=True) == expected)
    expected = 2*x1*x3*sin(2*x2)
    assert(LogicalExpr(dx1(M[2]), mapping=M, dim=rdim, subs=True) == expected)

    expected = -x1*(-k + 1)*sin(x2)
    assert(LogicalExpr(dx2(M[0]), mapping=M, dim=rdim, subs=True) == expected)
    expected = x1*(k + 1)*cos(x2)
    assert(LogicalExpr(dx2(M[1]), mapping=M, dim=rdim, subs=True) == expected)
    expected = 2*x1**2*x3*cos(2*x2)
    assert(LogicalExpr(dx2(M[2]), mapping=M, dim=rdim, subs=True) == expected)

    expected = 0
    assert(expand(LogicalExpr(dx3(M[0]), mapping=M, dim=rdim, subs=True)) == expand(expected))
    expected = 0
    assert(LogicalExpr(dx3(M[1]), mapping=M, dim=rdim, subs=True) == expected)
    expected = x1**2*sin(2*x2)
    assert(LogicalExpr(dx3(M[2]), mapping=M, dim=rdim, subs=True) == expected)

    expected = Matrix([[-2*D*x1 + (-k + 1)*cos(x2), -x1*(-k + 1)*sin(x2), 0],
                       [(k + 1)*sin(x2),             x1*(k + 1)*cos(x2), 0],
                       [2*x1*x3*sin(2*x2),           2*x1**2*x3*cos(2*x2), x1**2*sin(2*x2)]])
    assert(not( Jacobian(M) == expected))
    assert(expand(LogicalExpr(Jacobian(M), mapping=M, dim=rdim, subs=True)) == expand(expected))


#==============================================================================
# CLEAN UP SYMPY NAMESPACE
#==============================================================================
def teardown_module():
    from sympy import cache
    cache.clear_cache()

def teardown_function():
    from sympy import cache
    cache.clear_cache()
