import numpy as np
import cv2


TILE_SIZE = 32
OFS = 50

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

    background = np.zeros((700, 1000, 3), np.uint8)
    tiles = cv2.imread("tiles.png")

    market = SupermarketMap(MARKET, tiles)

    while True:
        frame = background.copy()
        market.draw(frame)

        cv2.imshow("frame", frame)

        key = chr(cv2.waitKey(1) & 0xFF)
        if key == "q":
            break

    cv2.destroyAllWindows()

    #market.write_image("supermarket.png")
