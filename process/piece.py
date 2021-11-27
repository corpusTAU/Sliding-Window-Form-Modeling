"""
Piece class, which, given metadata from db.py, loads musicXML files
and extracts sliding windows to create a large feature vector.
"""

import music21 as m21

from metadata.db_util import form_category
from process.bag_of_notes import BagOfNotes

DATA_PATH = "" # may need to change depending on working directory from which the code is run

class Piece():
    def __init__(self, metadata):
        # musxml, composer, catalogue, mvt, tonality, form, harmony_tsv=None
        self.composer = metadata["composer"]
        
        self.musxml = metadata["filename"]
        
        self.catalogue = metadata["CAT"]
        self.mvt = metadata["mvt"]
        self.tonality = metadata["tonality"]
        self.form = metadata["form"]
        self._form_category = None # this is used to override automatic form_category classification
    
    
    @property
    def title(self):
        return "{} {}".format(self.catalogue, self.mvt)
    
    @property
    def title_tonality(self):
        """ nice printing of a piece from the above dicts"""
        return "{} ({})".format(self.title, self.tonality)
    
    @property
    def is_major(self):
        return self.tonality[0] == self.tonality[0].upper()
    
    @property
    def form_category(self):
        # try to categorize form, unless explicitly specified by user
        if hasattr(self, "_form_category") and self._form_category is not None:
            return self._form_category
        return form_category(self.form)
    
    ########
    def load_xml(self):
        try:
            self.xml = m21.converter.parse(DATA_PATH + self.musxml)
            self.xml_metadata = {"title": self.xml.metadata.title,
                                 "composer": self.xml.metadata.composer,
                                 "highestTime": self.xml.highestTime}
        except:
            print(f"Error loading xml file at: {DATA_PATH + self.musxml}.")
            print("You may need to tweak piece.py/DATA_PATH in accordance with the current working directory.")
    
    def clear_xml(self): # for memory
        del self.xml
    
    
    ##### MusXML moving windows ####
    def grab_window(self, start, end):
        assert self.xml, "Must call Piece.load_xml() before calling grab_window()."
        
        window = self.xml.flat.getElementsByOffset(start, end,
                                                   includeEndBoundary=False,
                                                   mustFinishInSpan=False,
                                                   mustBeginInSpan=False,
                                                   includeElementsThatEndAtStart=False,
                                                   classList=[m21.note.Note, m21.chord.Chord]
                                                   )
        
        window_flat = []
        
        for note in window: # break up chords into notes
            if isinstance(note, m21.chord.Chord):
                for n in note:
                    if n.offset == 0:
                        n.offset += note.offset # hackish but necessary
                    window_flat.append(n)
            else:
                window_flat.append(note)
        
        
        bag = BagOfNotes()
        
        for note in window_flat: # TODO merge into previous loop
            if note.duration.quarterLength == 0:
                continue
            
            note_start = max(start, note.offset)
            note_end = min(end, note.offset+note.duration.quarterLength)
            if note_end < note_start:
                breakpoint()
            
            bag[note.name] += note_end - note_start
        
        
        return bag
    
    
    def compute_sliding_windows(self, num_windows, window_size):
        assert self.xml, "Must call Piece.load_xml() before calling grab_window()."
        
        self.windows = []
        
        window_size_in_quarters = self.xml.highestTime*window_size
        window_interval_in_quarters = 0 if num_windows == 1 else (self.xml.highestTime - window_size_in_quarters)/(num_windows-1)
        
        for n in range(num_windows):
            start = n*window_interval_in_quarters
            end = start + window_size_in_quarters
            
            bag = self.grab_window(start, end)
            
            self.windows.append(bag)
    
    
    def transpose_windows(self):
        assert self.tonality[0].upper() == self.tonality[0], "Transposition of minor pieces currently not supported."
        for b in self.windows:
            b.to_C(from_tonic=self.tonality)
        
    
    @property
    def min_key(self):
        assert self.windows
        return min([b.min_key for b in self.windows])
    
    @property
    def max_key(self):
        assert self.windows
        return max([b.max_key for b in self.windows])
    
    
    
    def windows_to_vector(self, min_key, max_key):
        big_vector = []
        
        for w in self.windows:
            # flatten returns a normalized distribution as a list
            # with zero-valued keys added to fill the entire range
            big_vector += w.flatten(min_key, max_key)
            
        self.features = big_vector
    
    
