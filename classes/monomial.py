from functools import total_ordering
import operator
import globals as glob


@total_ordering
class Monomial(list):

    def __init__(self, mono_pow):
        super().__init__()
        if len(mono_pow) == 0:
            raise Exception("Monomial must have at least one power.")
        for pow in mono_pow:
            self.append(pow)

    def deg(self):
        return sum(self)

    def copy(self):
        newMono = Monomial(self)
        return newMono

    def mul(self, other, out, pow=1):
        n = len(self)
        assert len(other) == n
        for i in range(n):
            out[i] = self[i] + pow * other[i]
        return out

    def __mul__(self, other, pow=1):
        result = Monomial([0] * len(self))
        return self.mul(other, result, pow)

    def __imul__(self, other, pow=1):
        return self.mul(other, self, pow)

    def __truediv__(self, other):
        return self.__mul__(other, -1)

    def __itruediv__(self, other):
        return self.__imul__(other, -1)

    def __pow__(self, pow):
        result = Monomial([0] * len(self))
        return self.mul(self, result, pow - 1)

    def __lt__(self, other):
        return self.__compar__(other, operator.lt, False, glob.MONOMIAL_ORDERING)

    def __gt__(self, other):
        return self.__compar__(other, operator.gt, False, glob.MONOMIAL_ORDERING)

    def __le__(self, other):
        return self.__compar__(other, operator.lt, True, glob.MONOMIAL_ORDERING)

    def __ge__(self, other):
        return self.__compar__(other, operator.gt, True, glob.MONOMIAL_ORDERING)

    def __eq__(self, other):
        n = len(self)
        assert len(other) == n
        for i in range(n):
            if self[i] != other[i]:
                return False
        return True

    def __compar__(self, other, comparfunc, equal: bool, order="lex"):
        if order == "lex":
            for pows, powo in zip(self, other):
                # we compare powers in reverse order because sort() orders values from small to large
                if comparfunc(powo, pows):
                    return True
                elif pows != powo:
                    return False
            return equal
        elif order == "deglex":
            if comparfunc(other.deg(), self.deg()):
                return True
            elif other.deg() == self.deg():
                return self.__compar__(other, comparfunc, equal, "lex")
            else:
                return False
        elif order == "degrevlex":
            if comparfunc(other.deg(), self.deg()):
                return True
            elif other.deg() == self.deg():
                for pows, powo in zip(self[::-1], other[::-1]):
                    if comparfunc(pows, powo):
                        return True
                    elif pows != powo:
                        return False
            else:
                return False
        else:
            raise Exception("Cannot order with " + order + ". Accepter orders are lex, deglex, degrevlex.")
