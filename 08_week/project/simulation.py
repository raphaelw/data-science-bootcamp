import math, cmath
import numpy as np
import cv2

"""
use parabola y = -(x*2-1)^2 + 1
draw stuff: https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
choice: https://stackoverflow.com/questions/40927221/how-to-choose-keys-from-a-python-dictionary-based-on-weighted-probability/40927437
"""

TILE_SIZE = 32
OFS = 50
FPS = 25

MARKET = """
##################
##..............##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##..##..##..##..##
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
##############GG##
""".strip()

class Ramp:
    """Ramps a float from 0 to 1 within n ticks."""
    def __init__(self):
        self.value = 0.
        self.step_size = 0.

    def reset(self, n_ticks):
        self.value = 0.
        self.step_size = 1./n_ticks

    def tick(self):
        self.value += self.step_size
        self.value = min(1.,self.value)
        return self.value
    
    def value(self):
        return self.value

    def done(self):
        if float(self.value) == float(1):
            return True
        return False

class Customer:
    def __init__(self):
        self.pos = 1.
        self._m = cmath.exp(1.j * 0.1)

    def tick(self):
        pass
    
    def draw(self, frame):
        self.pos *= self._m
        self.pos /= abs(self.pos) # stabilize

        cpos = self.pos * 60. + (100+100j)
        cpos = (round(cpos.real), round(cpos.imag))
        cv2.circle(frame, cpos, 4, (0,0,255), -1)

class SupermarketMap:
    """Visualizes the supermarket background"""

    def __init__(self, layout, tiles):
        """
        layout : a string with each character representing a tile
        tile   : a numpy array containing the tile image
        """
        self.tiles = tiles
        self.contents = [list(row) for row in layout.split("\n")]
        self.xsize = len(self.contents[0])
        self.ysize = len(self.contents)
        self.image = np.zeros(
            (self.ysize * TILE_SIZE, self.xsize * TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()

    def get_tile_by_location(self, col, row):
        """returns pixel array for tile in column (col) and row (row)"""
        col = int(col)
        row = int(row)
        return self.tiles[row * TILE_SIZE : (row+1) * TILE_SIZE, col * TILE_SIZE : (col+1) * TILE_SIZE]

    def get_tile(self, char):
        """returns the array for a given tile character"""

        if char == "#":
            return self.get_tile_by_location(0,0)
        elif char == "G":
            return self.get_tile_by_location(3,7)
        elif char == "C":
            return self.get_tile_by_location(8,2)
        elif char == "B": # banana
            return self.get_tile_by_location(4,0)
        
        return self.get_tile_by_location(2,1)


    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                bm = self.get_tile(tile)
                self.image[
                    y * TILE_SIZE : (y + 1) * TILE_SIZE,
                    x * TILE_SIZE : (x + 1) * TILE_SIZE,
                ] = bm

    def draw(self, frame, offset=OFS):
        """
        draws the image into a frame
        offset pixels from the top left corner
        """
        frame[
            OFS : OFS + self.image.shape[0], OFS : OFS + self.image.shape[1]
        ] = self.image

    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)


if __name__ == "__main__":
    frame_interval_ms = int(1000./FPS)

    background = np.zeros((700, 1000, 3), np.uint8)
    tiles = cv2.imread("tiles.png")

    customer = Customer()
    market = SupermarketMap(MARKET, tiles)

    while True:
        frame = background.copy()
        #market.draw(frame)
        customer.draw(frame)

        cv2.imshow("frame", frame)

        key = chr(cv2.waitKey(delay=frame_interval_ms) & 0xFF)
        if key == "q":
            break

    cv2.destroyAllWindows()

    #market.write_image("supermarket.png")
