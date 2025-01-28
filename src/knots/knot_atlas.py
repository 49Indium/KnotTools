from src.knots.knots import (
    Knot,
    TransverseCrossing,
    SingularCrossing,
    edges_from_sequence,
)

"""Standard trefoil"""
trefoil = Knot(
    [
        TransverseCrossing(0, 3, 5, 2, True),
        TransverseCrossing(4, 1, 3, 0, True),
        TransverseCrossing(2, 5, 1, 4, True),
    ],
    [(0, 1), (1, 2), (2, 0), (0, 1), (1, 2), (2, 0)],
)

two_chord = Knot(
    [
        SingularCrossing([5, 2], [0, 3]),
        SingularCrossing([3, 0], [4, 1]),
        TransverseCrossing(2, 5, 1, 4, True),
    ],
    [(0, 1), (1, 2), (2, 0), (0, 1), (1, 2), (2, 0)],
)
chord_3b = Knot(
    [
        SingularCrossing([4, 7], [5, 0]),
        SingularCrossing([0, 3], [1, 4]),
        TransverseCrossing(2, 7, 1, 6, True),
        SingularCrossing([5, 2], [6, 3]),
    ],
    [(0, 1), (1, 2), (2, 3), (3, 1), (1, 0), (0, 3), (3, 2), (2, 0)],
)
chord_3a = Knot(
    [
        SingularCrossing([2, 5], [3, 0]),
        SingularCrossing([0, 3], [1, 4]),
        SingularCrossing([4, 1], [5, 2]),
    ],
    [(0, 1), (1, 2), (2, 0), (0, 1), (1, 2), (2, 0)],
)
chord_3av2 = Knot(
    [
        SingularCrossing([2, 5], [3, 0]),
        SingularCrossing([0, 3], [1, 4]),
        SingularCrossing([4, 1], [5, 2]),
    ],
    edges_from_sequence([0, 1, 2, 0, 1, 2, 0]),
)

chord_4g = Knot(
    [
        SingularCrossing([8, 11], [9, 0]),
        SingularCrossing([0, 3], [1, 4]),
        SingularCrossing([4, 1], [5, 2]),
        TransverseCrossing(3, 6, 2, 5, True),
        TransverseCrossing(7, 10, 6, 9, True),
        SingularCrossing([10, 7], [11, 8]),
    ],
    edges_from_sequence([0, 1, 2, 3, 1, 2, 3, 4, 5, 0, 4, 5, 0]),
)
chord_4d = Knot(
    [
        SingularCrossing([9, 4], [0, 5]),
        SingularCrossing([7, 0], [8, 1]),
        SingularCrossing([1, 6], [2, 7]),
        SingularCrossing([5, 2], [6, 3]),
        TransverseCrossing(4, 9, 3, 8, True),
    ],
    edges_from_sequence([0, 1, 2, 3, 4, 0, 3, 2, 1, 4, 0]),
)
chord_4e = Knot(
    [
        SingularCrossing([7, 2], [0, 3]),
        SingularCrossing([0, 5], [1, 6]),
        SingularCrossing([4, 1], [5, 2]),
        SingularCrossing([3, 6], [4, 7]),
    ],
    edges_from_sequence([0, 1, 2, 0, 3, 2, 1, 3, 0]),
)
chord_4f = Knot(
    [
        SingularCrossing([2, 11], [3, 0]),
        TransverseCrossing(1, 6, 0, 5, True),
        SingularCrossing([6, 1], [7, 2]),
        TransverseCrossing(4, 9, 3, 8, True),
        SingularCrossing([9, 4], [10, 5]),
        SingularCrossing([7, 10], [8, 11]),
    ],
    edges_from_sequence([0, 1, 2, 0, 3, 4, 1, 2, 5, 3, 4, 5, 0]),
)
chord_4b = Knot(
    [
        SingularCrossing([4, 9], [5, 0]),
        TransverseCrossing(1, 8, 0, 7, True),
        SingularCrossing([6, 1], [7, 2]),
        SingularCrossing([2, 5], [3, 6]),
        SingularCrossing([8, 3], [9, 4]),
    ],
    edges_from_sequence([0, 1, 2, 3, 4, 0, 3, 2, 1, 4, 0]),
)
chord_4c = Knot(
    [
        SingularCrossing([9, 4], [0, 5]),
        SingularCrossing([5, 0], [6, 1]),
        SingularCrossing([1, 6], [2, 7]),
        TransverseCrossing(8, 3, 7, 2, True),
        SingularCrossing([3, 8], [4, 9]),
    ],
    edges_from_sequence([0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]),
)

chord_4a = Knot(
    [
        SingularCrossing([4, 11], [5, 0]),
        TransverseCrossing(8, 1, 7, 0, True),
        SingularCrossing([1, 6], [2, 7]),
        SingularCrossing([2, 9], [3, 10]),
        TransverseCrossing(11, 4, 10, 3, True),
        SingularCrossing([8, 5], [9, 6]),
    ],
    edges_from_sequence([0, 1, 2, 3, 4, 0, 5, 2, 1, 5, 3, 4, 0]),
)

trefoil_reversed = Knot(
    [
        TransverseCrossing(2, 5, 3, 0, False),
        TransverseCrossing(0, 3, 1, 4, False),
        TransverseCrossing(4, 1, 5, 2, False),
    ],
    [(1, 0), (2, 1), (0, 2), (1, 0), (2, 1), (0, 2)],
)

assignment_knot = Knot(
    [
        TransverseCrossing(5, 0, 4, 9, False),
        TransverseCrossing(1, 6, 0, 5, False),
        TransverseCrossing(7, 4, 6, 3, False),
        TransverseCrossing(3, 8, 2, 7, False),
        TransverseCrossing(9, 2, 8, 1, False),
    ],
    edges_from_sequence([0, 1, 4, 3, 2, 0, 1, 2, 3, 4, 0]),
)
