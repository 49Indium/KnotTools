from __future__ import annotations

import math
from itertools import zip_longest

# TODO make own class and consile with knots.py version
Fraction = tuple[int, int]


def reduce_fraction(frac: Fraction) -> Fraction:
    n = 2
    while n <= min(abs(frac[0]), abs(frac[1])):
        if frac[0] % n == 0 and frac[1] % n == 0:
            return reduce_fraction((frac[0] // n, frac[1] // n))
        n += 1
    return frac


class PolynomialOfSurd:
    surd: int
    lowest_power: int
    terms: list[int]

    def __init__(self, surd, lowest_power, terms) -> None:
        if surd < 1:
            raise ValueError(
                "Surds must be represented by a positive integer, indicating the nth root."
            )
        self.surd = surd
        self.lowest_power = lowest_power
        self.terms = terms

    def __repr__(self) -> str:
        n = self.lowest_power
        r = ""
        first_term = True
        for t in self.terms:
            if t != 0:
                if n % self.surd == 0:
                    r += f"{'' if first_term else ' + '}{t}t^{n // self.surd}"
                else:
                    r += f"{'' if first_term else ' + '}{t}t^{n}/{self.surd}"
                first_term = False
            n += 1
        if not r:
            return "0"
        return r

    def __eq__(self, __value: PolynomialOfSurd) -> bool:
        self._reduce_zero_terms()
        __value._reduce_zero_terms()
        if self.surd != __value.surd:
            return self.multiply_surd(__value.surd) == __value.multiply_surd(self.surd)
        if not self.terms and not __value.terms:
            return True
        return self.lowest_power == __value.lowest_power and self.terms == __value.terms

    def modified_polynomial_coefficient(self, i) -> int | Fraction:
        n = self.lowest_power
        r = 0
        for t in self.terms:
            if n != 0 and n % self.surd == 0:
                # TODO: Make this not round to integers but use fractions
                r += t * ((n // self.surd) ** i)
            n += 1

        if r % math.factorial(i) != 0:
            return reduce_fraction((r, math.factorial(i)))
        return r // math.factorial(i)

    def _set_lowest_power(self, i: int):
        n = max(0, self.lowest_power - i)
        self.lowest_power = min(i, self.lowest_power)
        self.terms = [0] * n + self.terms

    def _reduce_zero_terms(self):
        i = 0
        while self.terms and self.terms[0] == 0:
            i += 1
            self.lowest_power += 1
            self.terms.pop(0)

        while self.terms and self.terms[-1] == 0:
            self.terms.pop()

    def multiply_surd(self, k) -> PolynomialOfSurd:
        terms = [0] * (len(self.terms) * k - 1)
        terms[0::k] = self.terms
        return PolynomialOfSurd(k * self.surd, k * self.lowest_power, terms)

    def add(self, p: PolynomialOfSurd) -> PolynomialOfSurd:
        if self.surd != p.surd:
            return self.multiply_surd(p.surd).add(p.multiply_surd(self.surd))
        terms = [
            a + b
            for a, b in zip_longest(
                [0] * max(0, self.lowest_power - p.lowest_power) + self.terms,
                [0] * max(0, p.lowest_power - self.lowest_power) + p.terms,
                fillvalue=0,
            )
        ]
        return PolynomialOfSurd(
            self.surd, min(self.lowest_power, p.lowest_power), terms
        )

    def scale(self, k: int) -> PolynomialOfSurd:
        return PolynomialOfSurd(
            self.surd, self.lowest_power, [k * t for t in self.terms]
        )

    def subtract(self, p: PolynomialOfSurd) -> PolynomialOfSurd:
        return self.add(p.scale(-1))

    def multiply_by_power(self, n: int | Fraction):
        if isinstance(n, int):
            return self.multiply_by_power((n, 1))
        if n[1] != self.surd:
            return self.multiply_surd(n[1]).multiply_by_power(
                (n[0] * self.surd, n[1] * self.surd)
            )
        return PolynomialOfSurd(self.surd, self.lowest_power + n[0], list(self.terms))
