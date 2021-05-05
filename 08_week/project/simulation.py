import math, cmath, random
import numpy as np
import cv2

"""
use parabola y = -(x*2-1)^2 + 1
draw stuff: https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
transparency: https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c
choice: https://stackoverflow.com/questions/40927221/how-to-choose-keys-from-a-python-dictionary-based-on-weighted-probability/40927437
"""

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
        self._m = cmath.exp(1.j * 0.1 * random.random())

    def tick(self):
        self.pos *= self._m
        self.pos /= abs(self.pos) # stabilize
    
    def draw(self, frame):
        cpos = self.pos * 60. + (100+100j)
        cpos = (round(cpos.real), round(cpos.imag))
        cv2.circle(frame, cpos, 4, (0,0,255), -1)

        #if True:
        #    choice next state and duration

class SupermarketConductor:
    def __init__(self, num_of_customers):
        self.artists = [ Customer() for i in range(num_of_customers) ]

    def draw(self,frame):
        for artist in self.artists:
            artist.tick()
            artist.draw(frame)
    


def draw_tile(tiles, image, tile_row, tile_col, x, y, tile_size = 32):
    """
    Draw tile on an image.

    Parameters
    ----------
    tiles : 2D array
        tiles with size of tile_size
    image : 2D array
        tile is drawn on the image
    tile_row, tile_col : int
        select tile to draw
    x, y : int
        tile location on image
    """
    x = round(x-(tile_size/2))
    y = round(y-(tile_size/2))
    tile_row = int(tile_row)
    tile_col = int(tile_col)
    tile = tiles[tile_row * tile_size : (tile_row+1) * tile_size, tile_col * tile_size : (tile_col+1) * tile_size]
    image[y:y+tile_size , x:x+tile_size] = tile 

def prepare_supermarket_map(width=800, height=600):
    width = int(width)
    height = int(height)
    supermarket_map = {
         '_shape': {'width':width, 'height':height}
        ,'dairy': {
             'pos':(0.2*width, 0.5*height) # x,y
            ,'tile':(7,11) # row, col
        }
        ,'drinks': {
             'pos':(0.4*width, 0.5*height)
            ,'tile':(0,5)
        }
        ,'fruit': {
             'pos':(0.6*width, 0.5*height)
            ,'tile':(7,4)
        }
        ,'spices': {
             'pos':(0.8*width, 0.5*height)
            ,'tile':(2,3)
        }
        ,'entrance': {
             'pos':(0.5*width, 0.1*height)
            ,'tile':(1,1)
        }
        ,'checkout': {
             'pos':(0.5*width, 0.9*height)
            ,'tile':(2,8)
        }
    }

    image = np.zeros((height, width, 3), np.uint8)
    tiles = cv2.imread("tiles.png")

    for section in supermarket_map:
        if section.startswith('_'):
            continue

        x,y = map(round, supermarket_map[section]['pos'])
        supermarket_map[section]['pos'] = x,y
        tile_row, tile_col = supermarket_map[section]['tile']
        draw_tile(tiles=tiles, image=image, tile_row=tile_row, tile_col=tile_col, x=x, y=y)

    return image, supermarket_map

if __name__ == "__main__":
    fps = 25
    frame_interval_ms = int(1000./fps)

    background, supermarket_map = prepare_supermarket_map()

    composer = SupermarketConductor(30)

    while True:
        frame = background.copy()
        composer.draw(frame)

        cv2.imshow("frame", frame)

        key = chr(cv2.waitKey(delay=frame_interval_ms) & 0xFF)
        if key == "q":
            break

    cv2.destroyAllWindows()

    #market.write_image("supermarket.png")
