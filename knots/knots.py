from __future__ import annotations
from typing import Literal

import networkx as nx
import matplotlib.pyplot as plt
import random

VisitStatus = Literal["Half", "Visited"]
# (From, to)
Edge = tuple[int, int]
Loop = None
Segment = Edge | Loop


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


class SinglularCrossing:
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
            self.exiting[0], self.exiting[1], self.entering[0], self.entering[1], False
        )


Crossing = TransverseCrossing | SinglularCrossing


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
        return not any(isinstance(c, SinglularCrossing) for c in self.crossings)

    def split_singular_crossings(self) -> tuple[list[Knot], list[Knot]]:
        for i, crossing in enumerate(self.crossings):
            if isinstance(crossing, SinglularCrossing):
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
        if isinstance(crossing, SinglularCrossing):
            raise ValueError("A singular knot cannot be tranversed")
        return crossing.next_edge(current_index)

    def components(self) -> list[tuple[set[int], set[int]]]:
        result = []
        visited: set[int] = set()
        while len(visited) < len(self.edges):
            component_crossings: set[int] = set()
            component_edges: set[int] = set()
            current_index, current_edge = [
                (i, e) for i, e in enumerate(self.edges) if e not in visited
            ][0]
            while current_index not in visited:
                component_edges.add(current_index)
                if not current_edge:
                    break

                component_crossings.add(current_edge[1])
                crossing = self.crossings[current_edge[1]]
                if isinstance(crossing, SinglularCrossing):
                    raise ValueError(
                        "Components can only be found in non-singular knots"
                    )

                current_index = self.next_edge(current_index)

            result.append((component_crossings, component_edges))
        return result

    def draw(self):
        g = nx.MultiDiGraph()
        for i, crossing in enumerate(self.crossings):
            if isinstance(crossing, TransverseCrossing):
                g.add_node(i, type="Transverse", crossing_directions=crossing.strands())
            elif isinstance(crossing, SinglularCrossing):
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
trefoil_reversed = Knot(
    [
        TransverseCrossing(2, 5, 3, 0, False),
        TransverseCrossing(0, 3, 1, 4, False),
        TransverseCrossing(4, 1, 5, 2, False),
    ],
    [(1, 0), (2, 1), (0, 2), (1, 0), (2, 1), (0, 2)],
)
