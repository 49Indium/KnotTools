import unittest
import src.knots.knot_atlas as atlas
import src.knots.knots as k


class KnownKnotPropertiesTests(unittest.TestCase):

    def test_jones_polynomial(self):
        self.assertEqual(
            atlas.trefoil.jones_polynomial(), k.PolynomialOfSurd(1, 1, [1, 0, 1, -1])
        )
        self.assertEqual(
            atlas.trefoil_reversed.jones_polynomial(),
            k.PolynomialOfSurd(1, -4, [-1, 1, 0, 1]),
        )
        self.assertEqual(
            atlas.two_chord.jones_polynomial(),
            k.PolynomialOfSurd(1, 0, [-1, 1, 0, 1, -1]),
        )
        self.assertEqual(
            atlas.chord_3a.jones_polynomial(),
            k.PolynomialOfSurd(1, -4, [1, -1, 0, -1, 0, 1, 0, 1, -1]),
        )
        self.assertEqual(
            atlas.chord_3b.jones_polynomial(),
            k.PolynomialOfSurd(1, -2, [1, -1, -1, 0, 1, 1, -1]),
        )
        self.assertEqual(
            atlas.chord_4a.jones_polynomial(),
            k.PolynomialOfSurd(1, -2, [-1, 1, 2, -2, 1, -4, 4, -2, 2, -1]),
        )
        self.assertEqual(
            atlas.chord_4b.jones_polynomial(),
            k.PolynomialOfSurd(1, -4, [-1, 1, 1, 0, 0, -2, 0, 0, 1, 1, -1]),
        )
        self.assertEqual(
            atlas.chord_4c.jones_polynomial(),
            k.PolynomialOfSurd(1, -4, [-1, 1, 0, 1, 2, -4, 1, -4, 5, -1, 1, -1]),
        )
        self.assertEqual(
            atlas.chord_4d.jones_polynomial(),
            k.PolynomialOfSurd(1, -2, [-1, 1, 2, -1, -2, -1, 2, 1, -1]),
        )
        self.assertEqual(
            atlas.chord_4e.jones_polynomial(),
            k.PolynomialOfSurd(1, -4, [-1, 1, 2, -1, -2, -1, 2, 1, -1]),
        )
        self.assertEqual(
            atlas.chord_4f.jones_polynomial(),
            k.PolynomialOfSurd(1, 1, [-1, 3, -3, 2, -3, 3, -1]),
        )
        self.assertEqual(
            atlas.chord_4g.jones_polynomial(),
            k.PolynomialOfSurd(1, 0, [1, -2, 1, -2, 4, -2, 1, -2, 1]),
        )


if __name__ == "__main__":
    unittest.main()
