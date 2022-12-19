# courtesy of https://www.reddit.com/r/Python/comments/lw50ne/making_a_synthesizer_using_python/

class Panner:
    def __init__(self, r=0.5):
        self.r = r
        
    def __call__(self, val):
        r = self.r * 2
        l = 2 - r
        return (l * val, r * val)