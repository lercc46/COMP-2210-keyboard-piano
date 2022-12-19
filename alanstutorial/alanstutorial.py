# referencing:
    # https://www.reddit.com/r/Python/comments/lw50ne/making_a_synthesizer_using_python/

import itertools
import math
import numpy
import matplotlib.pyplot as plot

# sine wave generator using steps and an iterator
def get_sin_oscillator(freq, amp=1, phase=0, sample_rate=44100):
    phase = (phase / 360) * 2 * math.pi
    increment = (2 * math.pi * freq)/ sample_rate
    return (math.sin(phase + v) * amp for v in itertools.count(start=0, step=increment))

def main():

    osc = get_sin_oscillator(4)
    samples = [next(osc) for i in range(44100)]

    plot.plot(range(44100), samples)
    plot.title('sine')
    plot.xlabel('samples')
    plot.ylabel('amplitude')
    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')
    plot.show()

if __name__ == "__main__":
    main()