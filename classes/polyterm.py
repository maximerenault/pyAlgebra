from classes.monomial import Monomial
from functools import total_ordering


@total_ordering
class Polyterm(list[float, Monomial]):
    def __init__(self, factor: float, monomial: Monomial, variables: list = []) -> None:
        self.append(factor)
        self.append(monomial)
        self.variables = variables

    def deg(self):
        return self[1].deg()

    def copy(self):
        return Polyterm(self[0], self[1].copy(), self.variables)

    def __mul__(self, other):
        from classes.polynomial import Polynomial  # avoid circular imports

        if isinstance(other, Polyterm):
            return Polyterm(self[0] * other[0], self[1] * other[1], self.variables)
        elif isinstance(other, float) or isinstance(other, int):
            return Polyterm(self[0] * other, self[1], self.variables)
        elif isinstance(other, Polynomial):
            return other * self
        else:
            raise Exception("Cannot multiply Polyterm with" + str(type(other)))

    def __imul__(self, other):
        if isinstance(other, Polyterm):
            self[0] *= other[0]
            self[1] *= other[1]
        elif isinstance(other, float) or isinstance(other, int):
            self[0] *= other
        else:
            raise Exception("Cannot imultiply Polyterm with" + str(type(other)))
        return self

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Polyterm):
            return Polyterm(self[0] / other[0], self[1] / other[1], self.variables)
        elif isinstance(other, float) or isinstance(other, int):
            return Polyterm(self[0] / other, self[1], self.variables)
        else:
            raise Exception("Cannot divide Polyterm with" + str(type(other)))

    def __itruediv__(self, other):
        if isinstance(other, Polyterm):
            self[0] /= other[0]
            self[1] /= other[1]
        elif isinstance(other, float) or isinstance(other, int):
            self[0] /= other
        else:
            raise Exception("Cannot idivide Polyterm with" + str(type(other)))
        return self

    def __pow__(self, pow):
        if isinstance(pow, float) or isinstance(pow, int):
            return Polyterm(self[0] ** pow, self[1] ** pow, self.variables)
        else:
            raise Exception("Cannot take power of Polyterm with" + str(type(pow)))

    def __add__(self, other, sign=1):
        from classes.polynomial import Polynomial

        if isinstance(other, int) or isinstance(other, float):
            other = Polyterm(other, Monomial([0] * len(self[1])), self.variables)

        if self[1] == other[1]:
            return Polyterm(self[0] + sign * other[0], self[1], self.variables)
        elif len(self[1]) == len(other[1]):
            return Polynomial([self[0], sign * other[0]], [self[1], other[1]], self.variables)
        else:
            raise Exception("Cannot add Polyterm with " + str(type(other)))

    def __iadd__(self, other, sign=1):  # += operator
        assert self[1] == other[1]
        self[0] += sign * other[0]
        return self

    def __sub__(self, other):
        return self.__add__(other, -1)

    def __isub__(self, other):
        return self.__iadd__(other, -1)

    def __lt__(self, other):
        return self[1] < other[1] or (self[1] == other[1] and self[0] < other[0])

    def __gt__(self, other):
        return self[1] > other[1] or (self[1] == other[1] and self[0] > other[0])

    def __le__(self, other):
        return self[1] < other[1] or (self[1] == other[1] and self[0] <= other[0])

    def __ge__(self, other):
        return self[1] > other[1] or (self[1] == other[1] and self[0] >= other[0])

    def __eq__(self, other):
        if isinstance(other, Polyterm):
            return other[0] == self[0] and other[1] == other[1]
        elif isinstance(other, int):
            if other == 0 and self[0] == 0:
                return True
            else:
                return False
        else:
            raise Exception("Cannot compare Polyterm and " + str(type(other)))

    def __repr__(self) -> str:
        if self == 0:
            return str(0)
        if self[0] == 1:
            mystr = ""
        elif self[0] == -1:
            mystr = "-"
        else:
            mystr = f"{self[0]:.2f}"

        if self.variables == []:
            varnames = list(variable_names(len(self[1])))
        else:
            varnames = self.variables

        for i, pow in enumerate(self[1]):
            if pow != 0:
                if mystr != "" and mystr != "-":
                    mystr += "*"
                mystr += varnames[i]
                if pow > 1:
                    mystr += "**" + str(pow)

        if mystr == "-":
            mystr = "-1"
        return mystr

    def divisible_by(self, other):
        for pows, powo in zip(self[1], other[1]):
            if pows < powo:
                return False
        return True


def lcm(term1: Polyterm, term2: Polyterm):
    """Returns the least common multiple of term1 and term2."""
    monolcm = []
    for pow1, pow2 in zip(term1[1], term2[1]):
        monolcm.append(max(pow1, pow2))
    monolcm = Monomial(monolcm)
    lcm = Polyterm(1, monolcm, term1.variables)
    return lcm


def variable_names(dim):
    """Returns a list of variables for printing : x, y, z, xx, yy, zz, xxx, yyy..."""
    mychar = ["x", "y", "z"]
    for i in range(dim):
        mult = i // 3 + 1
        id = i % 3
        yield mychar[id] * mult


def symbols(unkn_str: str):
    """Returns a list of Polyterms with their names contained.
    Useful to construct a Polynomial in an intuitive manner.

    Example:
    x, y, z = symbols("x, y, z")
    Poly1 = x**2 + 4*x*y - 6*z"""
    unkn_list = unkn_str.split(", ")
    term_list = []
    n = len(unkn_list)
    for i in range(n):
        mono = Monomial([0] * n)
        mono[i] = 1
        term_list.append(Polyterm(1, mono, unkn_list))
    return term_list
