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

        def test_jones_polynomials_of_chords(self):
            chord_words = [
                (atlas.two_chord, [0,1,0,1]),
                (atlas.chord_3a, [0,1,2,0,1,2]),
                (atlas.chord_3b, [0,1,0,2,1,2]),
                (atlas.chord_4a, [0,1,2,0,3,1,3,2]),
                (atlas.chord_4b, [0,1,2,0,3,1,2,3]),
                (atlas.chord_4c, [0,1,2,3,0,1,2,3]),
                (atlas.chord_4d, [0,1,2,3,0,3,2,1]),
                (atlas.chord_4e, [0,1,2,3,1,0,3,2]),
                (atlas.chord_4f, [0,1,2,0,2,3,1,3]),
                (atlas.chord_4g, [0,1,2,3,2,3,0,1]),
            ]
            for chord_diagram, word in chord_words:
                self.assertEqual(chord_diagram.jones_polynomial(), k.Chord(word).to_knot().jones_polynomial())

if __name__ == "__main__":
    unittest.main()
