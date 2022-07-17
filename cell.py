class Cell:
    def __init__(self, size):
        self.size = size
        self.value = None
        self.candidates = set([x for x in range(1, size + 1)])

    def is_filled(self):
        return self.value is not None

    def set(self, num):
        self.value = num
        self.candidates = set([num])

    def clear(self):
        self.value = None
        self.candidates = set([x for x in range(1, self.size + 1)])

    def __sub__(self, candidate):
        self.candidates -= set([candidate])

    def __add__(self, candidate):
        self.candidates.add(candidate)

    def __contains__(self, val):
        return self.candidates.__contains__(val)

    def __eq__(self, other):
        return self.candidates == other.candidates

    def __str__(self):
        padded_set = " " * self.size
        # for val in self.candidates:
        #     padded_set = padded_set[:val - 1] + str(val) + padded_set[val:]
        if self.value is not None:
            padded_set = "." * (self.size // 2) + str(self.value) + "." * (self.size // 2 - 1 + self.size % 2)
        else:
            for val in self.candidates:
                padded_set = padded_set[:val - 1] + str(val) + padded_set[val:]
        return f"[{padded_set}]"