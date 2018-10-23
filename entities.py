from itertools import product
import random


class Cell:
    
    STATES = ['alive', 'dead']

    def __init__(self, x, y, state=None):
        self.x = x
        self.y = y
        self._state = random.choice(self.STATES) if state is None else state
        self.n_alive_neighbors = 0

    @property
    def is_alive(self):
        return bool(self)

    def __bool__(self):
        return self._state == 'alive'

    def __iter__(self):
        return (e for e in (self.x, self.y))

    def __str__(self):
        return '●' if self.is_alive else '○'

    def __repr__(self):
        return f'Cell(x={self.x}, y={self.y}, {self._state})'

    def evolve(self):
        if self.is_alive:
            if self.n_alive_neighbors < 2 or self.n_alive_neighbors > 3:
                self._state = 'dead'
        elif self.n_alive_neighbors == 3:
            self._state = 'alive'


class Grid:

    def __init__(self, height=50, width=50):
        self.height = height
        self.width = width
        self.iteration = 0
        self._content = self._build()

    def _build(self):
        return [
            [Cell(i, j) for i in range(self.width)]
            for j in range(self.height)
        ]

    def __str__(self):
        grid = '\n\n'  # separate new content
        for line in self._content:
            grid += ' '.join([str(cell) for cell in line]) + '\n'

        return grid

    def __getitem__(self, index):
        assert isinstance(index, tuple), 'Index must be a tuple of coordinates.'
        return self._content[index[1]][index[0]]

    def __iter__(self):
        return (cell for line in self._content for cell in line)

    def get_cell_neighbors(self, cell):
        x, y = cell
        neighbors = set()
        for i, j in product([-1, 0, 1], repeat=2):
            # We don't want negative index, just direct neighbors
            _x = max(x + i, 0)
            _y = max(y + j, 0)
            if _x == x and _y == y:  # cell itself, not a neighbor
                continue
            try:
                neighbors.add(self[(_x, _y)])
            except IndexError:  # beyond grid's edge
                continue

        return neighbors

    def count_alive_neighbors(self, cell):
        neighbors = self.get_cell_neighbors(cell)
        return sum(c.is_alive for c in neighbors)

    def update(self):
        for cell in self:
            cell.n_alive_neighbors = self.count_alive_neighbors(cell)

        self._update_state()
        self.iteration += 1

    def _update_state(self):
        for cell in self:
            cell.evolve()
            cell.n_alive_neighbors = 0

