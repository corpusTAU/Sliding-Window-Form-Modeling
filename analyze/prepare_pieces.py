"""

Load piece metadata, extract sliding window histograms from MusicXML files,
transposing and combining them into a large feature vector.

While the actual computations happen within the Piece class, the functions here
ensure coordination of preprocessing across the entire corpus (for example,
ensuring that feature vectors for all pieces in the corpus contain all pitch
classes appearing across the corpus).

"""

import pickle

from process.piece import Piece

pickle_path = "../db/"

def export_db(db, name):
    pickle.dump(db, open(pickle_path+name, "wb"))

def import_db(name):
    return pickle.load(open(pickle_path+name, "rb"))


def get_pieces(db):
    return [Piece(metadata) for metadata in db]




def compute_num_windows(window_size, overlap_percent):
    # computes number of windows
    # given window size (in percents of entire piece),
    # and percentage of overlap between neighboring windows
    # (w.r.t window size)
    return (100 - window_size) / (window_size*(1-overlap_percent/100)) + 1



### ================



def load_sliding_window_vectors(db, num_windows, window_size):
    db = get_pieces(db)
    
    for piece in db:
        print(f"Processing {piece.title}...")
        piece.load_xml()
        piece.compute_sliding_windows(num_windows, window_size)
        piece.clear_xml()
    
    return db



def transpose_db(db):
    # db shouldn't contain minor-mode pieces
    for piece in db:
        piece.transpose_windows()




def attach_feature_vector(db): # call load_sliding_window_vectors first
    min_key = min([piece.min_key for piece in db])
    max_key = max([piece.max_key for piece in db])
    
    for piece in db:
        piece.windows_to_vector(min_key, max_key)



#### helper functions for db import/export

def db_name(num_windows, window_size):
    """ Naming scheme for import/export preprocessed dbs for easier analysis.
    """
    # window_size is rounded and displayed as percentage
    return (f"MB_{num_windows}_{round(window_size*100)}.p")


def preprocess_db(num_windows, window_size):
    assert num_windows >= 1
    assert 0 < window_size <= 1
    
    # import metadata prior to feature extraction
    from metadata.db import Mozart_Beethoven_major
    
    # pick the set of all major-mode Mozart and Beethoven movements
    db = Mozart_Beethoven_major
    
    # extract bag-of-notes for each window of each piece
    load_sliding_window_vectors(db, num_windows, window_size)
    
    # normalize histograms so each piece would be in C major
    transpose_db(db) # db must only contain pieces in major mode!
    
    # normalizes windows into histograms, pads with zeros as necessary,
    # and concatenates to one long feature vector
    attach_feature_vector(db)
    
    # export the results to a file
    export_db(db, db_name(num_windows, window_size))






