from __future__ import annotations

class IncompatibleStacking(Exception):
    """An exception for when two objects (braids, tangles, etc) cannot be stacked due to the number of strands"""

    def __init__(self, message: str | None = None):
        self.message = (
            message
            or "Cannot vertically stack if there are a different numbers of strands"
        )
        super().__init__(self.message)


class Braid:
    n: int
    word: list[int]

    def __init__(self, n: int, word: list[int] | None = None):
        if n < 0:
            raise ValueError("Number of strands must be positive")
        if word and any(generator >= n or generator <= -n for generator in word):
            raise ValueError(
                f"Invalid generators in braid. Generators must be between {-n} and {n}"
            )
        self.n = n
        self.word = list(word) if word else []

    def __repr__(self) -> str:
        return f"Braid on {self.n} strands: {self.word}"

    def __str__(self) -> str:
        def print_generator(g):
            if g == 0:
                return "| " * (self.n - 1) + "|\n"
            
            crossing = " / " if g > 0 else " \\ "
            g = -g if g < 0 else g
            s = "| " * (g - 1) + "\\ /" + " |" * (self.n - (g - 1) - 2) + "\n"
            s += "| " * (g - 1) + crossing + " |" * (self.n - (g - 1) - 2) + "\n"
            s += "| " * (g - 1) + "/ \\" + " |" * (self.n - (g - 1) - 2) + "\n"
            return s
            
        s = ""
        for g in reversed(self.word):
            s = print_generator(0) + print_generator(g) + s
         
        return s + print_generator(0)

    def reduced_string(self) -> str:
        def print_generators(gens):
            s = ""
            for l in [0,1,2]:
                for i in range(self.n):
                    if i + 1 in gens or -i - 1 in gens:
                        if l == 0:
                            s += "\\ / "
                        elif l == 1 and i + 1 in gens:
                            s += " /  "
                        elif l == 1:
                            s += " \\  "
                        else:
                            s += "/ \\ "
                    elif i in gens or -i in gens:
                        pass
                    else:
                        s += "| "
                s.removesuffix(" ")
                s += "\n"
            return s
        
        def is_adjacent_generator(g, a):
            return abs(abs(g) - abs(a)) <= 1 and g != 0 and a != 0
        
        i = len(self.word) - 1
        s = ""
        while i >= 0:
            gens:list[int] = []
            while i >= 0 and not any(is_adjacent_generator(g, self.word[i]) for g in gens):
                gens.append(self.word[i])
                i -= 1
            s += "| " * (self.n - 1) + "|\n" + print_generators(gens)
        return s + "| " * (self.n - 1) + "|\n"

    @classmethod
    def identity(cls, n=1):
        return cls(n, [])

    def stack_under(self, b: Braid):
        if b.n != self.n:
            raise IncompatibleStacking(
                f"Cannot stack a braid of {self.n} strands under a braid of {b.n} strands"
            )
        return Braid(self.n, self.word + b.word)

    def stack_over(self, b: Braid):
        return b.stack_under(self)

    def conjoin_to_right(self, b: Braid):
        def shift_generator(generator, shift):
            if generator == 0:
                return generator
            elif generator > 0:
                return generator + shift
            else:
                return generator - shift
                
        return Braid(self.n + b.n, self.word + [shift_generator(g, self.n) for g in b.word])

    def conjoin_to_left(self, b: Braid):
        return b.conjoin_to_right(self)

    def reduce_inverses(self):
        l = len(self.word) + 1
        while len(self.word) < l:
            l = len(self.word)
            i = 0
            while i < len(self.word) - 1:
                if self.word[i] == -self.word[i+1]:
                    self.word.pop(i)
                    self.word.pop(i)
                else:
                    i += 1

    def reduce_identities(self):
        self.word = [a for a in self.word if a != 0]

    def simplify_word(self):
        self.reduce_identities()
        self.reduce_inverses()

    def inverse(self):
        return Braid(self.n, [-g for g in reversed(self.word)])
    
