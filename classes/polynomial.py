import bisect
from classes.monomial import Monomial
from classes.polyterm import Polyterm


class Polynomial(list[Polyterm]):

    def __init__(self, coeffs=[], powers=[], variables=[]):
        super().__init__()
        assert len(coeffs) == len(powers)

        for coeff, power in zip(coeffs, powers):
            if coeff != 0:
                self.append(Polyterm(coeff, Monomial(power), variables))

        self.sort()
        self.add_neighbors()
        self.delete_zeros()

    def deg(self):
        if len(self) == 0:
            return 0
        return self[0][1].deg()

    def reorder(self):
        self.sort()

    def dim(self):
        if len(self) == 0:
            return 0
        return len(self[0][1])

    def add_neighbors(self):
        n = len(self)
        for i in range(n - 1):
            term1 = self[i]
            term2 = self[i + 1]
            if term1[1] == term2[1]:
                term2 += term1
                self[i] = 0

    def delete_zeros(self):
        to_del = []
        for i, term in enumerate(self):
            if term == 0:
                to_del.append(i)
        for i in to_del[::-1]:
            self.pop(i)

    def lead(self):
        return self[0]

    def is_univariate(self):
        myvars = []
        for term in self:
            for i, var in enumerate(term[1]):
                if var and i not in myvars:
                    myvars.append(i)
        if len(myvars) > 1:
            return False
        return True

    def copy(self):
        newpoly = Polynomial()
        for term in self:
            newpoly.append(term.copy())
        return newpoly

    def add(self, other, out, sign=1):
        if isinstance(other, Polyterm):
            other = [other]
        elif isinstance(other, int) or isinstance(other, float):
            if len(self) == 0:
                raise Exception("You cannot start by adding an integer to a Polynomial, start with a Polyterm.")
            other = [Polyterm(other, Monomial([0] * len(self[0][1])), self[0].variables)]
        for term in other:
            i = bisect.bisect_left(out, term)
            if i != len(out) and out[i][1] == term[1]:
                out[i] += term * sign
            elif i != 0 and out[i - 1][1] == term[1]:
                out[i - 1] += term * sign
            else:
                out.insert(i, term * sign)
        out.delete_zeros()
        return out

    def __add__(self, other, sign=1):
        newpoly = self.copy()
        return self.add(other, newpoly, sign)

    def __iadd__(self, other, sign=1):
        return self.add(other, self, sign)

    def __sub__(self, other):
        return self.__add__(other, sign=-1)

    def __isub__(self, other):
        return self.__iadd__(other, sign=-1)

    def __mul__(self, other):
        def multerm(mterm):
            newpoly = self.copy()
            for term in newpoly:
                term *= mterm
            return newpoly

        if isinstance(other, Polyterm):
            other = [other]
        polysum = Polynomial()
        for term in other:
            polysum += multerm(term)
        return polysum

    def __truediv__(self, other):
        if isinstance(other, Polyterm) or isinstance(other, int) or isinstance(other, float):
            newpoly = self.copy()
            for term in newpoly:
                term /= other
            return newpoly
        else:
            raise Exception("Cannot divide Polynomial with " + str(type(other)))

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            for terms, termo in zip(self, other):
                if terms != termo:
                    return False
        elif isinstance(other, Polyterm) or isinstance(other, int) or isinstance(other, float):
            if len(self) == 1:
                return self[0] == other
            elif len(self) == 0 and other == 0:
                return True
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(repr(self))
