from sympy import Symbol
from sympy import sympify

from sympde.topology import Domain, ScalarFunctionSpace, element_of
from sympde.topology import dx, dy, dz
from sympde.topology import dx1, dx2, dx3
from sympde.topology import Mapping
from sympde.topology import DetJacobian
from sympde.topology import LogicalExpr
from sympde.topology import SymbolicExpr

#==============================================================================
def test_derivatives_2d_without_mapping():

    O = Domain('Omega', dim=2)
    V = ScalarFunctionSpace('V', O)
    u = element_of(V, 'u')

    expr = u
    assert SymbolicExpr(expr) == Symbol('u')

    expr = dx(u)
    assert SymbolicExpr(expr) == Symbol('u_x')

    expr = dx(dx(u))
    assert SymbolicExpr(expr) == Symbol('u_xx')

    expr = dx(dy(u))
    assert SymbolicExpr(expr) == Symbol('u_xy')

    expr = dy(dx(u))
    assert SymbolicExpr(expr) == Symbol('u_xy')

    expr = dy(dx(dz(u)))
    assert SymbolicExpr(expr) == Symbol('u_xyz')

    expr = dy(dy(dx(u)))
    assert SymbolicExpr(expr) == Symbol('u_xyy')

    expr = dy(dz(dy(u)))
    assert SymbolicExpr(expr) == Symbol('u_yyz')

#==============================================================================
def test_derivatives_2d_with_mapping():

    rdim = 2

    O = Domain('Omega', dim=rdim)
    V = ScalarFunctionSpace('V', O)
    u = element_of(V, 'u')

    M = Mapping('M', rdim)
    det_jac = DetJacobian(M)
    J = Symbol('J')

    expr = M
    assert SymbolicExpr(expr) == Symbol('M')

    expr = M[0]
    assert SymbolicExpr(expr) == Symbol('x')

    expr = M[1]
    assert SymbolicExpr(expr) == Symbol('y')

    expr = dx2(M[0])
    assert SymbolicExpr(expr) == Symbol('x_x2')

    expr = dx1(M[1])
    assert SymbolicExpr(expr) == Symbol('y_x1')

    expr       = LogicalExpr(M, dx(u)).subs(det_jac, J)
    expected   = '(u_x1 * y_x2 - u_x2 * y_x1)/J'
    difference = SymbolicExpr(expr) - sympify(expected)
    assert difference.simplify() == 0