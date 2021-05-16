# Markov chain Monte Carlo (MCMC)

Simulation of customers in a supermarket.

## How to run the animated simulation

```
python simulation.py
```

You can also render the animation to a video file:

```
python simulation.py -r path/to/video.mp4
```

## Dependencies

* OpenCV (opencv-python)

## How to adapt?

Different customer models can be simulated by implementing a simple duck type. See `customer.py` for examples.