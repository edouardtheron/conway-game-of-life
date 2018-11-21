import time

from models import Grid


def play(grid):
    while True:
        print(grid)
        time.sleep(0.5)
        grid.update()


def main():
    grid = Grid()
    play(grid)


if __name__ == '__main__':
    main()
