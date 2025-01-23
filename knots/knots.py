from __future__ import annotations
from typing import Literal
from itertools import zip_longest

import networkx as nx
import matplotlib.pyplot as plt
import random

VisitStatus = Literal["Half", "Visited"]
# (From, to)
Edge = tuple[int, int]
Loop = None
Segment = Edge | Loop


class Polynomial:
    lowest_power: int
    terms: list[int]

    def __init__(self, lowest_power, terms) -> None:
        self.lowest_power = lowest_power
        self.terms = terms

    def __repr__(self) -> str:
        n = self.lowest_power
        r = ""
        for t in self.terms:
            if n % 2 == 0:
                r += f" + {t}t^{n // 2}"
            else:
                r += f" + {t}t^{n}/2"
            n += 1
        return r

    def set_lowest_power(self, i: int):
        n = max(0, self.lowest_power - i)
        self.lowest_power = min(i, self.lowest_power)
        self.terms = [0] * n + self.terms

    def reduce_zero_terms(self):
        i = 0
        while self.terms and self.terms[0] == 0:
            i += 1
            self.lowest_power += 1
            self.terms.pop(0)

    def add(self, p: Polynomial):
        self.set_lowest_power(p.lowest_power)
        self.terms = [
            a + b
            for a, b in zip_longest(
                self.terms,
                [0] * max(0, p.lowest_power - self.lowest_power) + p.terms,
                fillvalue=0,
            )
        ]
        self.reduce_zero_terms()

    def scale(self, k: int):
        return Polynomial(self.lowest_power, [k * t for t in self.terms])

    def subtract(self, p: Polynomial):
        self.add(p.scale(-1))

    def multiply_by_power(self, n: int):
        return Polynomial(self.lowest_power + n, self.terms)


def change_edge(edge: Segment, min: int, amount: int):
    if not edge:
        return edge
    f = lambda e: e + amount if e > min else e
    return (f(edge[0]), f(edge[1]))


class TransverseCrossing:
    """
        out-under   out-over
                \\ /
                  /
                 / \\
          in-over  in-under
    """

    out_under: int
    out_over: int
    in_under: int
    in_over: int
    positive: bool

    def __init__(self, out_under, out_over, in_under, in_over, positive):
        self.out_under = out_under
        self.out_over = out_over
        self.in_under = in_under
        self.in_over = in_over
        self.positive = positive

    def __repr__(self) -> str:
        if self.positive:
            return f"""
                       {self.out_under}   {self.out_over}
                        \\ /
                         /
                        / \\
                       {self.in_over}  {self.in_under}
            """
        else:
            return f"""
                           {self.out_over}   {self.out_under}
                            \\ /
                             \\
                            / \\
                           {self.in_under}  {self.in_over}
                """

    def has_entry(self, edge: int) -> bool:
        """Don't allow for double entry"""
        return (self.in_under == edge) != (self.in_over == edge)

    def has_exit(self, edge: int) -> bool:
        """Don't allow for double exit"""
        return (self.out_under == edge) != (self.out_over == edge)

    def strands(self) -> list[int]:
        return [self.out_under, self.out_over, self.in_under, self.in_over]

    def out_strands(self) -> list[int]:
        return [self.out_under, self.out_over]

    def in_strands(self) -> list[int]:
        return [self.in_under, self.in_over]

    def next_edge(self, edge: int) -> int:
        if edge == self.in_over:
            return self.out_over
        elif edge == self.in_under:
            return self.out_under
        else:
            raise ValueError("Edge doesn't enter crossing")

    def change_edge_indexes(self, min: int, amount: int) -> TransverseCrossing:
        """Increase all edge indexes strictly above min by amount"""
        change_strand = lambda strand: strand + amount if strand > min else strand
        return TransverseCrossing(
            change_strand(self.out_under),
            change_strand(self.out_over),
            change_strand(self.in_under),
            change_strand(self.in_over),
            self.positive,
        )

    def replace_input(self, old_edge: int, new_edge: int) -> TransverseCrossing:
        if self.in_under == old_edge:
            return TransverseCrossing(
                self.out_under, self.out_over, new_edge, self.in_over, self.positive
            )
        elif self.in_over == old_edge:
            return TransverseCrossing(
                self.out_under, self.out_over, self.in_under, new_edge, self.positive
            )
        else:
            raise ValueError("Cannot replace edge that doesn't exist")


class SingularCrossing:
    """
        Written such that:
        exiting[0]   exiting[1]
                 \\ /
                   o
                  / \\
        entering[1]  entering[0]
    """

    entering: list[int]
    exiting: list[int]

    def __init__(self, entering, exiting):
        if len(entering) != 2:
            raise ValueError("Incorrect number of entering strands")
        if len(exiting) != 2:
            raise ValueError("Incorrent number of exiting strands")
        self.entering = list(entering)
        self.exiting = list(exiting)

    def __repr__(self) -> str:
        return f"""
                   {self.exiting[0]}   {self.exiting[1]}
                    \\ /
                     o
                    / \\
                   {self.entering[1]}  {self.entering[0]}
        """

    def has_entry(self, edge: int) -> bool:
        return edge in self.entering and self.entering != [edge, edge]

    def has_exit(self, edge: int) -> bool:
        return edge in self.exiting and self.exiting != [edge, edge]

    def strands(self) -> list[int]:
        return self.entering + self.exiting

    def out_strands(self) -> list[int]:
        return list(self.exiting)

    def in_strands(self) -> list[int]:
        return list(self.entering)

    def positive_version(self) -> TransverseCrossing:
        return TransverseCrossing(
            self.exiting[0], self.exiting[1], self.entering[0], self.entering[1], True
        )

    def negative_version(self) -> TransverseCrossing:
        return TransverseCrossing(
            self.exiting[1], self.exiting[0], self.entering[1], self.entering[0], False
        )

    def change_edge_indexes(self, min: int, amount: int) -> SingularCrossing:
        """Increase all edge indexes strictly above min by amount"""
        change_strand = lambda strand: strand + amount if strand > min else strand
        return SingularCrossing(
            [change_strand(e) for e in self.entering],
            [change_strand(e) for e in self.exiting],
        )


Crossing = TransverseCrossing | SingularCrossing


class Knot:
    crossings: list[Crossing]
    edges: list[Segment]

    def __init__(self, crossings: list[Crossing], edges: list[Segment]) -> None:
        seen: set[int] = set()
        for i, crossing in enumerate(crossings):
            for exiting_strand_index in crossing.out_strands():
                exiting_strand = edges[exiting_strand_index]
                seen.add(exiting_strand_index)
                if exiting_strand not in edges:
                    raise ValueError(f"Edge listed in crossing, but not provided")
                if not exiting_strand:
                    raise ValueError("Crossing has an outgoing loop")
                if not crossings[exiting_strand[1]].has_entry(exiting_strand_index):
                    raise ValueError(
                        f"Crossing number {i} has an outgoing strand {exiting_strand}, but this strand does not enter crossing {exiting_strand[1]}."
                    )
            for entering_strand_index in crossing.in_strands():
                entering_strand = edges[entering_strand_index]
                seen.add(entering_strand_index)
                if entering_strand not in edges:
                    raise ValueError(f"Edge listed in crossing, but not provided")
                if not entering_strand:
                    raise ValueError("Crossing has an incoming loop")
                if not crossings[entering_strand[0]].has_exit(entering_strand_index):
                    raise ValueError(
                        f"Crossing number {i} has an ingoing strand {entering_strand}, but this strand does not enter crossing {entering_strand[0]}."
                    )

        for i, edge in enumerate(edges):
            if edge and i not in seen:
                raise ValueError(
                    f"Edge {edge} was provided but was not connected to any crossings"
                )

        self.crossings = crossings
        self.edges = edges

    def is_singular(self) -> bool:
        return any(isinstance(c, SingularCrossing) for c in self.crossings)

    def swap_crossing(self, index: int) -> Knot:
        crossing = self.crossings[index]
        new_crossings = list(self.crossings)
        if isinstance(crossing, SingularCrossing):
            raise ValueError("You cannot swap a singular crossing")
        if crossing.positive:
            new_crossings[index] = TransverseCrossing(
                crossing.out_over,
                crossing.out_under,
                crossing.in_over,
                crossing.in_under,
                False,
            )
        else:
            new_crossings[index] = TransverseCrossing(
                crossing.out_over,
                crossing.out_under,
                crossing.in_over,
                crossing.in_under,
                True,
            )
        return Knot(new_crossings, list(self.edges))

    def untwist_crossing(self, index: int) -> Knot:
        crossing = self.crossings[index]
        new_crossings = list(self.crossings)
        new_edges = list(self.edges)
        if isinstance(crossing, SingularCrossing):
            raise ValueError("You cannot untwist a singular crossing")

        # TODO Do you need separate cases for left and right
        if crossing.out_under == crossing.in_over:
            new_edges[crossing.out_under] = None
        else:
            left_in_edge = new_edges[crossing.in_over]
            left_out_edge = new_edges[crossing.out_under]
            new_edges[crossing.in_over] = (left_in_edge[0], left_out_edge[1])
            new_crossings[left_out_edge[1]] = new_crossings[
                left_out_edge[1]
            ].replace_input(crossing.out_under, crossing.in_over)

            new_edges.pop(crossing.out_under)
            new_crossings = [
                c.change_edge_indexes(crossing.out_under, -1) for c in new_crossings
            ]

        # Update the crossing
        crossing = new_crossings[index]

        if crossing.out_over == crossing.in_under:
            new_edges[crossing.out_over] = None
        else:
            right_in_edge = new_edges[crossing.in_under]
            right_out_edge = new_edges[crossing.out_over]
            new_edges[crossing.in_under] = (right_in_edge[0], right_out_edge[1])
            new_crossings[right_out_edge[1]] = new_crossings[
                right_out_edge[1]
            ].replace_input(crossing.out_over, crossing.in_under)

            new_edges.pop(crossing.out_over)
            new_crossings = [
                c.change_edge_indexes(crossing.out_over, -1) for c in new_crossings
            ]

        new_crossings.pop(index)
        new_edges = [change_edge(e, index, -1) for e in new_edges]

        return Knot(new_crossings, new_edges)

    def split_singular_crossings(self) -> tuple[list[Knot], list[Knot]]:
        for i, crossing in enumerate(self.crossings):
            if isinstance(crossing, SingularCrossing):
                positive_version = list(self.crossings)
                positive_version[i] = crossing.positive_version()
                negative_version = list(self.crossings)
                negative_version[i] = crossing.negative_version()

                (a, b) = Knot(
                    positive_version, list(self.edges)
                ).split_singular_crossings()
                (c, d) = Knot(
                    negative_version, list(self.edges)
                ).split_singular_crossings()

                return (a + d, b + c)

        return ([Knot(list(self.crossings), list(self.edges))], [])

    def next_edge(self, current_index: int) -> int:
        current_edge = self.edges[current_index]
        if not current_edge:
            raise ValueError("Linked to loop")
        crossing = self.crossings[current_edge[1]]
        if isinstance(crossing, SingularCrossing):
            raise ValueError("A singular knot cannot be tranversed")
        return crossing.next_edge(current_index)

    def components(self) -> list[tuple[set[int], set[int]]]:
        result = []
        visited: set[int] = set()
        while len(visited) < len(self.edges):
            component_crossings: set[int] = set()
            component_edges: set[int] = set()
            current_index = [i for i, _ in enumerate(self.edges) if i not in visited][0]
            while current_index not in visited:
                component_edges.add(current_index)
                visited.add(current_index)
                current_edge = self.edges[current_index]

                if not current_edge:
                    break

                component_crossings.add(current_edge[1])
                crossing = self.crossings[current_edge[1]]
                if isinstance(crossing, SingularCrossing):
                    raise ValueError(
                        "Components can only be found in non-singular knots"
                    )

                current_index = self.next_edge(current_index)

            result.append((component_crossings, component_edges))
        return result

    def disjoint_sum(self, k: Knot):
        new_crossings = self.crossings + [
            c.change_edge_indexes(-1, len(self.edges)) for c in k.crossings
        ]
        new_edges = self.edges + [
            change_edge(e, -1, len(self.crossings)) for e in k.edges
        ]
        return Knot(new_crossings, new_edges)

    def remove_component(self, component: tuple[set[int], set[int]]):
        new_crossings = list(self.crossings)
        new_edges = list(self.edges)

        seen: set[int] = set()
        for crossing_index in component[0]:
            seen.add(crossing_index)
            crossing_index -= len([i for i in seen if i < crossing_index])
            new_edges = [change_edge(e, crossing_index, -1) for e in new_edges]

        seen: set[int] = set()
        for edge_index in component[1]:
            seen.add(edge_index)
            edge_index -= len([i for i in seen if i < edge_index])
            new_crossings = [
                c.change_edge_indexes(edge_index, -1) for c in new_crossings
            ]

        for crossing_index in sorted(list(component[0]), reverse=True):
            new_crossings.pop(crossing_index)
        for edge_index in sorted(list(component[1]), reverse=True):
            new_edges.pop(edge_index)

        return Knot(new_crossings, new_edges)

    def remove_edges(self, edges: list[int]):
        crossings = {}
        for e in edges:
            if self.edges[e][1] in crossings:
                crossings[self.edges[e][1]] += 1
            else:
                crossings[self.edges[e][1]] = 1

        new_crossings = list(self.crossings)
        new_edges = list(self.edges)
        for c, count in sorted(
            list(crossings.items()), key=lambda x: x[0], reverse=True
        ):
            if count == 1:
                strands = [s for s in new_crossings[c].strands() if s not in edges]
                if strands[0] == strands[1]:
                    new_edges[strands[0]] = None
                else:
                    a = [s for s in strands if new_edges[s][1] == c][0]
                    b = [s for s in strands if new_edges[s][0] == c][0]
                    new_edges[a] = (new_edges[a][0], new_edges[b][1])
                    new_crossings[new_edges[a][1]] = new_crossings[
                        new_edges[a][1]
                    ].replace_input(b, a)
                    new_edges.pop(b)
                    edges = [(e - 1 if e > b else e) for e in edges]
                    new_crossings = [
                        c.change_edge_indexes(b, -1) for c in new_crossings
                    ]

                new_edges = [change_edge(e, c, -1) for e in new_edges]
                new_crossings.pop(c)
            else:
                new_edges = [change_edge(e, c, -1) for e in new_edges]
                new_crossings.pop(c)
        for e in sorted(list(edges), reverse=True):
            new_crossings = [c.change_edge_indexes(e, -1) for c in new_crossings]
            new_edges.pop(e)
        return Knot(new_crossings, new_edges)

    def jones_polynomial(self) -> Polynomial:
        if self.is_singular():
            pos, neg = self.split_singular_crossings()
            p = Polynomial(0, [])
            for k in pos:
                print(
                    f"Calculated pos {k.crossings} {k.edges} to be {k.jones_polynomial()}"
                )
                p.add(k.jones_polynomial())
            for k in neg:
                print(
                    f"Calculated neg {k.crossings} {k.edges} to be {k.jones_polynomial()}"
                )
                p.subtract(k.jones_polynomial())
            return p

        if not self.edges:
            return Polynomial(0, [1])

        if len(self.edges) == 1 and not self.edges[0]:
            return Polynomial(0, [1])

        if not self.edges[0]:
            k = self.remove_component((set(), {0}))
            p = Polynomial(0, [])
            q = k.jones_polynomial()
            p.subtract(q.multiply_by_power(1))
            p.subtract(q.multiply_by_power(-1))
            return p

        seen_edges: set[int] = set()
        seen_crossings: set[int] = set()
        current_edge: int = 0

        while current_edge not in seen_edges:
            seen_edges.add(current_edge)
            current_crossing = self.edges[current_edge][1]
            if current_edge == self.crossings[current_crossing].in_over:
                current_edge = self.crossings[current_crossing].out_over
                seen_crossings.add(current_crossing)
            elif current_crossing in seen_crossings:
                current_edge = self.crossings[current_crossing].out_under
            elif self.crossings[current_crossing].positive:
                p = Polynomial(0, [])
                r = self.swap_crossing(current_crossing).jones_polynomial()
                p.add(r.multiply_by_power(4))
                q = self.untwist_crossing(current_crossing).jones_polynomial()
                p.add(q.multiply_by_power(3))
                p.subtract(q.multiply_by_power(1))
                return p
            else:
                p = Polynomial(0, [])
                p.add(
                    self.swap_crossing(current_crossing)
                    .jones_polynomial()
                    .multiply_by_power(-4)
                )
                q = self.untwist_crossing(current_crossing).jones_polynomial()
                p.add(q.multiply_by_power(-3))
                p.subtract(q.multiply_by_power(-1))
                return p

        k = self.remove_edges(list(seen_edges))
        if not k.edges:
            return Polynomial(0, [1])
        p = Polynomial(0, [])
        q = k.jones_polynomial()
        p.subtract(q.multiply_by_power(1))
        p.subtract(q.multiply_by_power(-1))
        return p

    def draw(self):
        g = nx.MultiDiGraph()
        for i, crossing in enumerate(self.crossings):
            if isinstance(crossing, TransverseCrossing):
                g.add_node(i, type="Transverse", crossing_directions=crossing.strands())
            elif isinstance(crossing, SingularCrossing):
                g.add_node(i, type="Singular")
            else:
                raise ValueError("Unknown crossing type")

        loops = len(self.crossings)
        arrows = ["" for _ in self.edges]
        for i, edge in enumerate(self.edges):
            if not edge:
                g.add_node(loops, type="Loop")
                loops += 1
            else:
                g.add_edge(edge[0], edge[1])
                previous_crossing = self.crossings[edge[0]]
                next_crossing = self.crossings[edge[0]]
                from_over = (
                    isinstance(previous_crossing, TransverseCrossing)
                    and previous_crossing.out_over == i
                )
                from_under = (
                    isinstance(previous_crossing, TransverseCrossing)
                    and previous_crossing.out_under == i
                )
                to_over = (
                    isinstance(next_crossing, TransverseCrossing)
                    and next_crossing.in_over == i
                )
                to_under = (
                    isinstance(next_crossing, TransverseCrossing)
                    and next_crossing.in_under == i
                )
                arrow = ""
                if from_under:
                    arrow += "]"
                arrow += "-"
                if to_under:
                    arrow += "["
                else:
                    arrow += ">"
                arrows[i] = arrow

        nx.draw(
            g,
            arrowstyle=arrows,
            connectionstyle=[
                f"arc3,rad={random.uniform(-0.8,0.8)}" for _ in self.edges
            ],
        )
        plt.show()


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
trefoil_reversed = Knot(
    [
        TransverseCrossing(2, 5, 3, 0, False),
        TransverseCrossing(0, 3, 1, 4, False),
        TransverseCrossing(4, 1, 5, 2, False),
    ],
    [(1, 0), (2, 1), (0, 2), (1, 0), (2, 1), (0, 2)],
)
