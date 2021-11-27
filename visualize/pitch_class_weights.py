"""

Given a feature vector of a single piece (or average of a set of pieces),
visualize the relative weight of each PC in the piece across time.
A separate curve is drawn for each PC, tracing its weight per sliding window.
To prevent clatter, the less significant PCs are filtered out.

"""


def visualize_window_vector(vector, min_key, max_key, title=None):
    from math import floor, ceil
    from utils import int_to_pitch
    import numpy as np
    import matplotlib.pyplot as plt
    
    plt.rcParams['savefig.dpi'] = 800
    
    distinct_pcs = max_key-min_key+1
    num_windows = int(len(vector)/distinct_pcs)
    
    plt.figure()
    if not title is None:
        plt.title(title)
    
    max_peak = 0.13 # default minimum; this is for axis limits only
    text_y_margin = 0.005 # distance between PC label and corresponding graph peak
    
    shuffle = [floor(distinct_pcs/2) + ceil(i/2)*(-1)**i for i in range(distinct_pcs)] # hack to choose nicer colors
    
    for pc in shuffle:
        ys = [vector[pc + distinct_pcs*w] for w in range(num_windows)]
        
        peak = np.max(ys)
        peak_x = np.argmax(ys)
        
        if peak > max_peak: max_peak = peak
        
        if pc + min_key in range(-3, 8): # only show Eb - C#
            plt.plot(ys)
            plt.text(peak_x,
                     peak + text_y_margin,
                     int_to_pitch(pc+min_key),
                     ha='left' if peak_x/num_windows < 0.02 else ('right' if peak_x/num_windows > 0.98 else 'center') )
            plt.plot([peak_x, peak_x], [peak, peak+text_y_margin-0.0015], 'black')
        
    
    plt.axis([0, num_windows-1, 0, max_peak])
    plt.show()



