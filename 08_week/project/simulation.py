import math, cmath, random
import queue
from functools import partial
import numpy as np
import cv2

from customer import CustomerModel

""" NOTES
draw stuff: https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html
transparency: https://gist.github.com/IAmSuyogJadhav/305bfd9a0605a4c096383408bee7fd5c
choice: https://stackoverflow.com/questions/40927221/how-to-choose-keys-from-a-python-dictionary-based-on-weighted-probability/40927437
"""

# Smoothstep functions https://en.wikipedia.org/wiki/Smoothstep
smoothstep = lambda x: x * x * (3 - 2 * x)
smootherstep = lambda x: x * x * x * (x * (x * 6 - 15) + 10)
vector_transform = lambda x, src, dest: src + smootherstep(x)*(dest-src)

def bezier_transform(x, src, dest, ctrl):
    """
    3-point Bezier Curve with De Casteljau’s algorithm.
    For details see https://javascript.info/bezier-curve

    x : scalar in range [0,1]
    src, dest, ctrl : vector
    """
    line1 = vector_transform(x,src,ctrl)
    line2 = vector_transform(x,ctrl,dest)
    return vector_transform(x,line1,line2)

def get_fancy_transformer(src, src_ideal, dest, scale_vertical_offset=1.2):
    """Helper function for bezier based transform. Returns a function."""
    ctrl = src_ideal + 0.5*(dest-src_ideal)
    scale_vertical_offset *= -1.*np.sign(dest[0]-ctrl[0])
    ctrl[1] += np.linalg.norm(dest-ctrl)*scale_vertical_offset

    return partial(bezier_transform, src=src, dest=dest, ctrl=ctrl)

class Ramp:
    """Ramps a float from 0 to 1 within n ticks and applies a transform to it."""
    def __init__(self, n_ticks=10, transformer=smoothstep):
        self.n_ticks = int(n_ticks)
        self._transformer = transformer
        self.reset(n_ticks)

    def reset(self, n_ticks=None):
        self._value = 0.
        n_ticks = self.n_ticks if n_ticks == None else n_ticks
        self._step_size = 1./n_ticks

    def tick(self):
        self._value += self._step_size
        self._value = min(1.,self._value)
        return self.position()
    
    def position(self):
        return self._transformer(self._value)

    def done(self):
        if float(self._value) == 1:
            return True
        return False

class TransformerWiggleWaggle:
    def __init__(self, center_pos=(0,0), deviation=1, n_ticks=100, interval_ticks=20):
        self._center_pos = np.array(center_pos, dtype=float)
        self._deviation = float(deviation)
        self._ramp = Ramp(n_ticks=int(n_ticks))
        self._interval_ticks = int(interval_ticks)
        self._tick_counter = 0

        self._noise = np.zeros_like(self._center_pos)
        self._noise_dest = np.zeros_like(self._noise)

    def tick(self):
        self._ramp.tick()

        new_noise = self._tick_counter == 0
        self._tick_counter = (self._tick_counter+1) % self._interval_ticks

        if new_noise:
            self._noise_dest = (2*np.random.random(2)-1) * self._deviation

        # Exponential Moving Average : y[n] = (1-alpha)*x[n] + alpha*y[n-1]
        alpha = 0.9
        self._noise = (1.-alpha)*self._noise_dest + alpha*self._noise

    def position(self):
        return self._center_pos + self._noise

    def done(self):
        return self._ramp.done()

def position(supermarket, section):
    return np.array( supermarket[section]['pos'] , dtype=float )

class CustomerView:
    def __init__(self, supermarket_map):
        self._map = supermarket_map
        self._model = CustomerModel()
        
        self._transformer_queue = queue.Queue()
        self._transformer = None

        section, self._duration = self._model.get_state()
        self._pos = position(self._map, section)

    def _next_transition(self):
        last_section = self._model.get_state()[0]

        # proceed model to next state
        self._model.next_state()
        section, duration = self._model.get_state()

        dest = position(self._map, section)
        src = self._pos
        last_section_info = self._map[last_section]
        section_info = self._map[section]

        # put transformations (aka animations) into the queue
        t = partial(vector_transform, src=self._pos, dest=dest)
        if last_section_info['type'] == 'section' and section_info['type'] == 'section':
            # do fancy transition
            last_ideal_pos = np.array(last_section_info['pos'], dtype=float)
            t = get_fancy_transformer(src=self._pos, src_ideal=last_ideal_pos, dest=dest, scale_vertical_offset=1.5)

        transformer = Ramp(n_ticks=30, transformer=t)
        self._transformer_queue.put(transformer)

        # spend time in state
        transformer = TransformerWiggleWaggle(center_pos=np.array(section_info['pos'], dtype=float)
                                             , deviation=50
                                             , n_ticks=200
                                             , interval_ticks=5)
        self._transformer_queue.put(transformer)

    def tick(self):
        if self._transformer is not None:
            if self._transformer.done():
                self._transformer = None
            else:
                self._transformer.tick()
        
        if self._transformer is None:
            if self._transformer_queue.empty():
                # all transformations done
                self._next_transition()
            else:
                # get next queue element
                self._transformer = self._transformer_queue.get(block=False)
    
    def draw(self, frame):
        if self._transformer is not None:
            self._pos = self._transformer.position()

        pos = tuple(self._pos.astype(int))
        cv2.circle(frame, pos, 4, (255,255,255), -1)


class SupermarketConductor:
    def __init__(self, num_of_customers, supermarket_map):
        self.artists = [ CustomerView(supermarket_map=supermarket_map) for i in range(num_of_customers) ]

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
    image[ y:y+tile_size , x:x+tile_size ] = tile 


def prepare_supermarket_map(width=1000, height=800):
    width = int(width)
    height = int(height)
    supermarket_map = {
         '_shape': {'width':width, 'height':height}
        ,'dairy': {
             'pos':(0.2*width, 0.5*height) # x,y
            ,'tile':(7,11) # row, col
            ,'type':'section'
        }
        ,'drinks': {
             'pos':(0.4*width, 0.5*height)
            ,'tile':(6,13)
            ,'type':'section'
        }
        ,'fruit': {
             'pos':(0.6*width, 0.5*height)
            ,'tile':(7,4)
            ,'type':'section'
        }
        ,'spices': {
             'pos':(0.8*width, 0.5*height)
            ,'tile':(2,3)
            ,'type':'section'
        }
        ,'entrance': {
             'pos':(0.5*width, 0.1*height)
            ,'tile':(1,1)
            ,'type':'other'
        }
        ,'checkout': {
             'pos':(0.5*width, 0.9*height)
            ,'tile':(2,8)
            ,'type':'other'
        }
    }

    background = np.zeros((height, width, 3), np.uint8)
    image = background.copy()
    tiles = cv2.imread("tiles.png")

    for section in supermarket_map:
        if section.startswith('_'):
            continue

        x,y = map(round, supermarket_map[section]['pos'])
        supermarket_map[section]['pos'] = x,y

        tile_row, tile_col = supermarket_map[section]['tile']
        draw_tile(tiles=tiles, image=image, tile_row=tile_row, tile_col=tile_col, x=x, y=y)

    # alpha / transparency
    alpha = 0.5
    image = cv2.addWeighted(image, alpha, background, 1-alpha, 0)

    return image, supermarket_map

if __name__ == "__main__":
    fps = 25
    frame_interval_ms = int(1000./fps)

    background, supermarket_map = prepare_supermarket_map()

    composer = SupermarketConductor(30, supermarket_map)

    while True:
        frame = background.copy()
        composer.draw(frame)

        cv2.imshow("frame", frame)

        key = chr(cv2.waitKey(delay=frame_interval_ms) & 0xFF)
        if key == "q":
            break

    cv2.destroyAllWindows()

    #market.write_image("supermarket.png")
