from classes.polyterm import symbols
from polynomial_division import buchberger, reduce_GB
import globals

if __name__ == "__main__":

    globals.MONOMIAL_ORDERING = "lex"  # "lex", "deglex" or "degrevlex"

    x, y = symbols("x, y")
    p1 = x**3 - 2 * x * y
    p2 = x**2 * y - 2 * y**2 + x
    G = [p1, p2]

    G_basis = buchberger(G)
    G_reduced = reduce_GB(G_basis)
    print("Reduced Basis :", G_reduced)

    x, y, z = symbols("x, y, z")
    p1 = x**2 + y + z - 1
    p2 = x + y**2 + z - 1
    p3 = x + y + z**2 - 1
    G = [p1, p2, p3]

    G_basis = buchberger(G)
    G_reduced = reduce_GB(G_basis)
    print("Reduced Basis :", G_reduced)

    # Doesn't work
    # w0, w1, x0, y0, x1, y1 = symbols("w0, w1, x0, y0, x1, y1")
    # p1 = w0 + w1 - 1
    # p2 = w0 * y0 + w1 * y1 - 1 / 3
    # p3 = w0 * x0 + w1 * x1 - 1 / 3
    # p4 = w0 * x0 * y0 + w1 * x1 * y1 - 1 / 12
    # p5 = w0 * x0**2 + w1 * x1**2 - 1 / 6
    # p6 = w0 * y0**2 + w1 * y1**2 - 1 / 6
    # G = [p1, p2, p3, p4, p5, p6]

    # G_basis = buchberger(G)
    # G_reduced = reduce_GB(G_basis)
    # print("Reduced Basis :", G_reduced)

    # Comparison with sympy
    from sympy.solvers import solve
    from sympy import symbols as symsymbols, groebner

    x, y, z = symsymbols("x, y, z")
    p1 = x**2 + y + z - 1
    p2 = x + y**2 + z - 1
    p3 = x + y + z**2 - 1
    G = [p1, p2, p3]
    print(groebner(G, x, y, z))
    print(solve(G, x, y, z))

    w0, w1, x0, y0, x1, y1 = symsymbols("w0, w1, x0, y0, x1, y1")
    p1 = w0 + w1 - 1
    p2 = w0 * y0 + w1 * y1 - 1 / 3
    p3 = w0 * x0 + w1 * x1 - 1 / 3
    p4 = w0 * x0 * y0 + w1 * x1 * y1 - 1 / 12
    p5 = w0 * x0**2 + w1 * x1**2 - 1 / 6
    p6 = w0 * y0**2 + w1 * y1**2 - 1 / 6
    G = [p1, p2, p3, p4, p5, p6]
    print(groebner(G, w0, w1, x0, y0, x1, y1))  # Should return [1]
    print(solve(G, w0, w1, x0, y0, x1, y1))  # Should return []

    # Doesn't work
    # w0, w1, w2, x0, y0, x1, y1, x2, y2 = symsymbols("w0, w1, w2, x0, y0, x1, y1, x2, y2")
    # p1 = w0 + w1 + w2 - 1
    # p2 = w0 * y0 + w1 * y1 + w2 * y2 - 1 / 3
    # p3 = w0 * x0 + w1 * x1 + w2 * x2 - 1 / 3
    # p4 = w0 * x0 * y0 + w1 * x1 * y1 + w2 * x2 * y2 - 1 / 12
    # p5 = w0 * x0**2 + w1 * x1**2 + w2 * x2**2 - 1 / 6
    # p6 = w0 * y0**2 + w1 * y1**2 + w2 * y2**2 - 1 / 6
    # G = [p1, p2, p3, p4, p5, p6]
    # print(groebner(G, w0, w1, w2, x0, y0, x1, y1, x2, y2), order="grevlex")
    # print(solve(G, w0, w1, w2, x0, y0, x1, y1, x2, y2))
