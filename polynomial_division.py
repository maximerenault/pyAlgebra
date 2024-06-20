import copy
import itertools
from classes.polynomial import Polynomial
from classes.polyterm import lcm


def euclidean_division(Dividende: Polynomial, Divisor: Polynomial) -> tuple[Polynomial, Polynomial]:
    """Returns Euclidean division's quotient and rest for univariate polynomials."""
    assert Dividende.dim() == Divisor.dim() == 1
    assert Divisor != Polynomial()
    q = Polynomial()
    r = Dividende.copy()
    while r != Polynomial() and r.deg() >= Divisor.deg():
        t = r.lead() / Divisor.lead()  # Divide the leading terms
        q += t
        r -= Divisor * t

    return (q, r)


def s_poly(poly1, poly2):
    """Calculate the S-polynomial for poly1 and poly2."""
    mylcm = lcm(poly1.lead(), poly2.lead())
    s = mylcm * (poly1 / poly1.lead() - poly2 / poly2.lead())
    return s


def multidiv(poly: Polynomial, Polys: list[Polynomial]):
    """Mutlivariate multi division from this video https://youtu.be/xP9dM06JeoA."""
    n = len(Polys)
    Q = [Polynomial()] * n
    r = Polynomial()
    p = poly.copy()
    i = 0
    while p != 0:
        if p.lead().divisible_by(Polys[i].lead()):
            t = p.lead() / Polys[i].lead()
            Q[i] += t
            p -= t * Polys[i]
            i = 0
        i += 1
        if i == n:
            r += p.lead()
            p -= p.lead()
            i = 0
    return r, Q


def buchberger(Polys: list[Polynomial]):
    """Buchberger's Algorithm from this video https://youtu.be/KzT2S9er93k"""
    G = copy.deepcopy(Polys)
    pairs = list(itertools.combinations(G, 2))  # replace list by set for unordered
    while pairs:
        p, q = pairs.pop()
        s = s_poly(p, q)
        r, _ = multidiv(s, G)
        if r != 0:
            for g in G:
                pairs.append((g, r))  # append for list, add for set
            G.append(r)
    return G


def reduce_GB(G):
    """Reduces a Groebner basis so that the leading terms of the basis don't divide each other."""
    temp = copy.deepcopy(G)
    G_minimal = []
    while temp:
        p = temp.pop()
        if not any([p.lead().divisible_by(q.lead()) for q in temp + G_minimal]):
            G_minimal.append(p)

    n = len(G_minimal)
    G_reduced = []
    for i in range(n):
        r, _ = multidiv(G_minimal[i], G_minimal[:i] + G_minimal[i + 1 :])
        if r != 0:
            G_reduced.append(r)
    return G_reduced
