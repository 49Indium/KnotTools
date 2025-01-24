# Knot Tools

A python library to help you study knots and calculate their invariants.

Allows you to represent knots, links and braids (tangles coming soon), combine them together and calculate their invariants. Created during whilst studying the Algebraic Knot Theory course at the [2025 AMSI Summer School](https://ss.amsi.org.au/) to gain a better understanding and help computations. More documentation and features coming in the next few days as I add more to it.

# Example Usage

```python
import knots.knots as *

# A bunch of knots are already included
print(trefoil.jones_polynomial())
# Returns 1t^1 + 1t^3 + -1t^4

# An example knot from one of the assignments
# Knots consist of a list of crossings, each with the corresponding edges attached, and whether they are positive or negative. 
# They also contain a list of edges, to help determine when crossings are connected.
assignment_knot = Knot(
    [
        TransverseCrossing(5, 0, 4, 9, False),
        TransverseCrossing(1, 6, 0, 5, False),
        TransverseCrossing(7, 4, 6, 3, False),
        TransverseCrossing(3, 8, 2, 7, False),
        TransverseCrossing(9, 2, 8, 1, False) # A negative crossing
    ],
    edges_from_sequence([0, 1, 4, 3, 2, 0, 1, 2, 3, 4, 0])
)

print(assignment_knot.jones_polynomial().modified_polynomial_coefficient(4))
# Returns (-65, 2), which represents -65/2

# One of the knots equivalent to the chord diagram corresponding to ABCDCBAD
# Crossings can be singular or transverse
chord_diagram_example = Knot(
    [
        SingularCrossing([9, 4], [0, 5]),
        SingularCrossing([7, 0], [8, 1]),
        SingularCrossing([1, 6], [2, 7]),
        SingularCrossing([5, 2], [6, 3]),
        TransverseCrossing(4, 9, 3, 8, True) # A positive crossing
    ],
    edges_from_sequence([0, 1, 2, 3, 4, 0, 3, 2, 1, 4, 0])
)

print(assignment_knot.jones_polynomial())
# Returns -1t^-2 + 1t^-1 + 2t^0 + -1t^1 + -2t^2 + -1t^3 + 2t^4 + 1t^5 + -1t^6

```
