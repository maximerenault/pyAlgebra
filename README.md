# pyAlgebra

A small computational algebra library in Python that allows the computation of Groebner basis for lex, deglex or degrevlex monomial ordering. It is composed of three classes : Polynomial, Polyterm and Monomial of which names are quite self-explanatory. They only work with int and floating point approximation (no rational numbers) and there is no way to specify the Ring we want them to live in. Examples of usage are in main.py.

## Introduction to computational algebra

This library is not at all made for production use, but I hope it can help people who are looking for clues on computational algebra. It is not, however, destined to be a very precise course, but more of a sketch that leads to the right ideas.

### Ring

Let's start with the definition of a **Ring**. It is nothing more than a set to which we appended an **addition** and a **multiplication**. The polynomial Ring is then the set of polynomials which allows their addition and multiplication. It can be based on Q, R or C, meaning that our coefficients live in these sets. We generally call the variables constituting our polynomials _indeterminates_, but having more of an analytical interest in polynomials, I will continue using "variable".

### Ideal

From an element of the polynomial Ring, or a set of elements, we define the ideal generated as all the polynomials obtained from addition or multiplication of these elements.

### Monomial ordering

Monomials are elements of the polynomial Ring only made of variables such as $x^2$ or $xy^3z$. Ordering them is very important as it will dictate which terms are in the front line, and will be targeted by our elimination process. For univariate polynomials it is straightforward : $x^4+5x^2-2$ the **leading term** being $x^4$.

For multivariate polynomial you have options :

- Lexicographic ordering, or **lex**. Simply in alphabetical order : $x^2y+xy^2-xyz-y^4+y^3$. Notice how $-y^4$ is pushed back in the polynomial, although it is of higher degree that the leading term.
- Degree lexicographic order or **deglex**. Same thing but considering the degree first : $-y^4+x^2y+xy^2-xyz+y^3$.
- Degree reverse lexicographic order or **degrevlex**. Same thing but we use the lexicographic ordering in reverse and we reverse again the result. This is a bit confusing, let's make it in two steps. First the reverse lex putting z first, then y and finally x : $-y^4-xyz+y^3+xy^2+x^2y$ and the inversion $-y^4+x^2y+xy^2+y^3-xyz$.

### Basis of an Ideal

Solving a polynomial system of equations is like finding the roots of the Ideal generated by these polynomials, and thus having a good basis for the ideal, will make it easier to find the roots. A basis for the Ideal is a set of polynomials which generates the ideal, so or base polynomials form indeed a basis, but not necessarily an easy one to solve for.

### Gröbner basis

A Gröbner basis is a particular basis which has very interesting properties. It is formally defined as the basis of the Ideal I of which the leading terms form a basis for the Ideal of the leading terms of the polynomials in I.

The definition doesn't seem very interesting, but its properties are very uncommon. Finding a reduced Gröbner basis (meaning we removed the redundant polynomials) is exactly like Gaussian elimination in linear systems, except it is a lot more difficult to do. With a lex ordering, it allows us to extract a univariate polynomial which can be solved (with a QR algorithm) and its roots injected in another polynomial which in turn becomes univariate, etc. Unfortunately the lex ordering is also the most difficult ordering to compute a Gröbner basis for.

For a problem with no solution, the Gröbner basis will reduce to zero. And for a 1 or higher-dimensional problem, the basis will not exhibit one univariate polynomial.

To compute a Gröbner basis, one should look into Buchberger's algorithm.

## Example

To compute the Gröbner basis from a set of polynomials one can proceed like this :

    from classes.polyterm import symbols
    from polynomial_division import buchberger, reduce_GB
    import globals

    globals.MONOMIAL_ORDERING = "lex"  # "lex", "deglex" or "degrevlex"

    x, y = symbols("x, y")
    p1 = x**3 - 2 * x * y
    p2 = x**2 * y - 2 * y**2 + x
    G = [p1, p2]

    G_basis = buchberger(G)
    G_reduced = reduce_GB(G_basis)
    print("Reduced Basis :", G_reduced)
