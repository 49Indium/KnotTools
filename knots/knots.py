from __future__ import annotations
from typing import Literal


VisitStatus = Literal["Half", "Visited"]


class PointCrossing:
    num: int

    def __init__(self, num):
        self.num = num

    def has_entry(self, crossing):
        return crossing == self.num

    def has_exit(self, crossing):
        return crossing == self.num

    def strands(self):
        return [self.num, self.num]

    def out_strands(self):
        return [self.num]

    def in_strands(self):
        return [self.num]


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

    def has_entry(self, crossing):
        """Don't allow for double entry"""
        return (self.in_under == crossing) != (self.in_over == crossing)

    def has_exit(self, crossing):
        """Don't allow for double exit"""
        return (self.out_under == crossing) != (self.out_over == crossing)

    def strands(self):
        return [self.out_under, self.out_over, self.in_under, self.in_over]

    def out_strands(self):
        return [self.out_under, self.out_over]

    def in_strands(self):
        return [self.in_under, self.in_over]


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

    def has_entry(self, crossing):
        return crossing in self.entering and self.entering != [crossing, crossing]

    def has_exit(self, crossing):
        return crossing in self.exiting and self.exiting != [crossing, crossing]

    def strands(self):
        return self.entering + self.exiting

    def out_strands(self):
        return list(self.exiting)

    def in_strands(self):
        return list(self.entering)

    def positive_version(self):
        return TransverseCrossing(
            self.exiting[0], self.exiting[1], self.entering[0], self.entering[1], True
        )

    def negative_version(self):
        return TransverseCrossing(
            self.exiting[0], self.exiting[1], self.entering[0], self.entering[1], False
        )


Crossing = PointCrossing | TransverseCrossing | SinglularCrossing


class Knot:
    crossings: list[Crossing]

    def __init__(self, crossings: list[Crossing]) -> None:
        for i, crossing in enumerate(crossings):
            for exiting_strand in crossing.out_strands():
                if not crossings[exiting_strand].has_entry(i):
                    raise ValueError(
                        f"Crossing number {i} has an outgoing strand to {exiting_strand}, but this strand does not enter this crossing."
                    )
            for entering_strand in crossing.in_strands():
                if not crossings[entering_strand].has_exit(i):
                    raise ValueError(
                        f"Crossing number {i} has an ingoing strand from {entering_strand}, but this strand does not exit this crossing."
                    )

        self.crossings = crossings

    def is_singular(self) -> bool:
        return not any(isinstance(c, SinglularCrossing) for c in self.crossings)

    def split_singular_crossings(self) -> tuple[list[Knot], list[Knot]]:
        for i, crossing in enumerate(self.crossings):
            if isinstance(crossing, SinglularCrossing):
                positive_version = list(self.crossings)
                positive_version[i] = crossing.positive_version()
                negative_version = list(self.crossings)
                negative_version[i] = crossing.negative_version()

                (a, b) = Knot(positive_version).split_singular_crossings()
                (c, d) = Knot(negative_version).split_singular_crossings()

                return (a + d, b + c)

        return ([Knot(list(self.crossings))], [])

    def next_crossing(self, current_crossing: int, currently_over: bool) -> int:
        crossing = self.crossings[current_crossing]
        if isinstance(crossing, TransverseCrossing):
            if currently_over:
                return crossing.out_over
            else:
                return crossing.out_under
        elif isinstance(crossing, PointCrossing):
            return current_crossing
        elif isinstance(crossing, SinglularCrossing):
            raise ValueError("A singular knot cannot be tranversed")
        raise ValueError("Unknown crossing type")

    def components(self) -> list[int]:
        result = []
        visited: dict[int, VisitStatus] = {}
        while len(visited) < len(self.crossings):
            component = []
            is_over = True
            current = [i for i in range(len(self.crossings)) if i not in visited][0]
            crossing = self.crossings[current]
            while current not in visited or visited[current] != "Visited":
                if isinstance(crossing, TransverseCrossing):
                    if current not in visited:
                        visited[current] = "Half"
                    else:
                        visited[current] = "Visited"
                elif isinstance(crossing, PointCrossing):
                    visited[current] = "Visited"
                else:
                    raise ValueError(
                        "Components can only be found in non-singular knots"
                    )

                previous = current
                current = self.next_crossing(current, is_over)
                crossing = self.crossings[current]
                if isinstance(crossing, TransverseCrossing):
                    is_over = crossing.in_over == previous
            result.append(component)
        return result
