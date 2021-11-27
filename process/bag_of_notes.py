"""
Container for collecting notes and deriving histograms from them.
"""

from utils import pitch_to_int

class BagOfNotes():
    """ A container counting amounts of pitch classes.
    Keys are internally stored as ints but on the user end both are possible.
    """
    def __init__(self):
        self.pitches = {}
    
    def __getitem__(self, pitch):
        return self.pitches.get(pitch_to_int(pitch), 0)
    
    def __setitem__(self, pitch, value):
        assert value >= 0 # sanity check
        self.pitches[pitch_to_int(pitch)] = value
    
    #### methods with side effects:
    
    def merge(self, src, dest):
        """ identify src pitch with dest pitch,
        combining the values of both.
        e.g.: w.merge(12,0) consider occurrences of B#s as Cs.
        """
        src = pitch_to_int(src)
        dest = pitch_to_int(dest)
        
        self.pitches[dest] += self.pitches[src]
        del self.pitches[src]
    
    
    def collapse_to_range(self, _min, _max):
        """
        ensures all keys are in range [_min, _max]
        """
        
        assert _max - _min >= 12
        rng = range(_min, _max+1)
        to_change = [p for p in self.pitches if p not in rng]
        for p in to_change:
            dest = p
            while dest not in rng:
                dest += 12*(-1 if dest > _max else 1)
            
            self.merge(p, dest)
    
    def to_C(self, from_tonic):
        """ Transposes to C major from the given major scale.
        w.to_C(from_tonic="E") transposes down a major third.
        """
        delta = pitch_to_int(from_tonic)
        self.pitches = {p-delta:self.pitches[p] for p in self.pitches}
    
    #### no side effects:
    @property
    def PCs(self):
        return set(self.pitches.keys())
    
    @property
    def min_key(self):
        return min(self.pitches.keys())
    
    @property
    def max_key(self):
        return max(self.pitches.keys())
    
    def dist(self, min_key=None, max_key=None):
        """ No side effects.
        Normalizes pitches and returns as probability distribution (dict).
        Use min_key/max_key to expand keys cover some required range.
        """
        assert min_key is None or min_key <= self.min_key
        assert max_key is None or max_key >= self.max_key
        
        min_key = self.min_key if min_key is None else min(min_key, self.min_key)
        max_key = self.max_key if max_key is None else max(max_key, self.max_key)
        
        total = sum(self.pitches.values())
        return {p:self[p]/total for p in range(min_key, max_key+1)}
    
    def flatten(self, min_key=None, max_key=None):
        """ No side effects.
        Returns normalized distribution as a list.
        """
        d = self.dist(min_key, max_key)
        return [d[p] for p in sorted(list(d.keys()))]
