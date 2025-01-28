import unittest
from src.knots.polynomials import *
from hypothesis import given, strategies as st


def polynomial(
    surd_min=1,
    surd_max=10,
    least_degree=-10,
    highest_degree=10,
    max_number_of_terms=10,
    min_term_coefficient=100,
    max_term_coefficient=100,
):
    return st.builds(
        PolynomialOfSurd,
        st.integers(surd_min, surd_max),
        st.integers(least_degree, highest_degree),
        st.lists(
            st.integers(min_term_coefficient, max_term_coefficient),
            max_size=max_number_of_terms,
        ),
    )


class PolynomialTests(unittest.TestCase):
    @given(polynomial())
    def test_reducing_zeros_is_identity(self, p: PolynomialOfSurd):
        q = PolynomialOfSurd(p.surd, p.lowest_power, p.terms)
        q._reduce_zero_terms()
        self.assertEqual(p, q)

    @given(polynomial(), st.integers(0, 10), st.integers(0, 10))
    def test_equality_with_zero_padding(self, p: PolynomialOfSurd, a: int, b: int):
        self.assertEqual(
            p,
            PolynomialOfSurd(
                p.surd, p.lowest_power - a, ([0] * a) + p.terms + ([0] * b)
            ),
        )

    @given(polynomial(), st.integers(1, 10))
    def test_equality_with_surd_change(self, p: PolynomialOfSurd, k: int):
        self.assertEqual(p, p.multiply_surd(k))

    @given(polynomial(), st.integers(1, 10), st.integers(1, 10))
    def test_surd_multiplication_sommutativity(
        self, p: PolynomialOfSurd, k: int, l: int
    ):
        self.assertEqual(
            p.multiply_surd(k).multiply_surd(l), p.multiply_surd(l).multiply_surd(k)
        )

    @given(polynomial(), polynomial())
    def test_addition_on_polynomials_commutes(
        self, p: PolynomialOfSurd, q: PolynomialOfSurd
    ):
        self.assertEqual(p.add(q), q.add(p))

    @given(polynomial(), polynomial(), polynomial())
    def test_addition_on_polynomials_is_associative(
        self, p: PolynomialOfSurd, q: PolynomialOfSurd, r: PolynomialOfSurd
    ):
        self.assertEqual(p.add(q.add(r)), p.add(q).add(r))

    @given(polynomial(), st.integers(1, 10), st.integers(0, 100), st.integers(-10, 10))
    def test_addition_on_polynomials_has_identity(
        self, p: PolynomialOfSurd, surd: int, terms: int, lowest: int
    ):
        self.assertEqual(p, p.add(PolynomialOfSurd(surd, lowest, [0] * terms)))
        self.assertEqual(p, PolynomialOfSurd(surd, lowest, [0] * terms).add(p))

    @given(polynomial(), st.integers(), st.integers())
    def test_scaling_polynomials_commutes(self, p: PolynomialOfSurd, k: int, l: int):
        self.assertEqual(p.scale(k).scale(l), p.scale(l).scale(k))

    @given(polynomial())
    def test_scaling_polynomials_has_identity(self, p: PolynomialOfSurd):
        self.assertEqual(p, p.scale(1))

    @given(polynomial(), polynomial(), st.integers())
    def test_scaling_polynomials_distributes_over_addition(
        self, p: PolynomialOfSurd, q: PolynomialOfSurd, k: int
    ):
        self.assertEqual(p.add(q).scale(k), p.scale(k).add(q.scale(k)))

    @given(polynomial(), polynomial(), st.integers())
    def test_scaling_polynomials_distributes_over_subtraction(
        self, p: PolynomialOfSurd, q: PolynomialOfSurd, k: int
    ):
        self.assertEqual(p.subtract(q).scale(k), p.scale(k).subtract(q.scale(k)))

    @given(polynomial(), polynomial())
    def test_subtraction_on_polynomials_is_additive_inverse(
        self, p: PolynomialOfSurd, q: PolynomialOfSurd
    ):
        self.assertEqual(PolynomialOfSurd(1, 0, []), p.subtract(p))
        self.assertEqual(p, p.subtract(q).add(q))
        self.assertEqual(p, p.add(q).subtract(q))

    # TODO: Make fraction strategy
    @given(polynomial(), st.integers(-10, 10), st.integers(1, 10))
    def test_power_multiplication_has_inverse(
        self, p: PolynomialOfSurd, numerator: int, denominator: int
    ):
        self.assertEqual(
            p,
            p.multiply_by_power((numerator, denominator)).multiply_by_power(
                (-numerator, denominator)
            ),
        )

    @given(polynomial())
    def test_power_multiplication_has_identity(self, p: PolynomialOfSurd):
        self.assertEqual(p, p.multiply_by_power(0))
        self.assertEqual(p, p.multiply_by_power((0, 1)))

    @given(polynomial(), polynomial(), st.integers(-10, 10), st.integers(1, 10))
    def test_increading_power_polynomials_distributes_over_addition(
        self, p: PolynomialOfSurd, q: PolynomialOfSurd, numerator: int, denominator: int
    ):
        self.assertEqual(
            p.add(q).multiply_by_power((numerator, denominator)),
            p.multiply_by_power((numerator, denominator)).add(
                q.multiply_by_power((numerator, denominator))
            ),
        )

    @given(polynomial(), polynomial(), st.integers(-10, 10), st.integers(1, 10))
    def test_increading_power_polynomials_distributes_over_subtraction(
        self, p: PolynomialOfSurd, q: PolynomialOfSurd, numerator: int, denominator: int
    ):
        self.assertEqual(
            p.subtract(q).multiply_by_power((numerator, denominator)),
            p.multiply_by_power((numerator, denominator)).subtract(
                q.multiply_by_power((numerator, denominator))
            ),
        )

    # TODO: Test modified polynomial coefficient
