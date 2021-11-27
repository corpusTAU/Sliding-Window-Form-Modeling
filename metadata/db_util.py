"""

Functionality for filtering of db.py, and classifying form labels into
the 3 major categories and "Misc".

"""

def form_category(form):
    if form in ("Sonata", "Sonata_with_intro", "Slow_sonata", "Sonata_rondo",
                "Slow_sonatina", "9_part_rondo", "2_tempo_sonata", "5_part_sonata_rondo"):
        return "Sonata"
    
    if form in ("Minuet&Trio", "Slow_ABA", "Rondo_ABA", "Scherzo&Trio", "Minuet/Scherzo&Trio"):
        return "ABA"
    
    if form in ("Variations",):
        return "Variations"
    
    if form in ("5_part_rondo", "Binary_varied_repeats", "Reigen_rondo", "Fugue_with_intro", 
                "Free_cantilena", "Rounded_binary", "7_part_rondo"):
        return "Misc"
    
    print(f"Can't categorize form: {form}")
    return NotImplemented


# for filtering db
def is_major(piece): return piece["tonality"][0].isupper()
def is_first(piece): return piece['mvt'] == 'i'
def is_second(piece): return piece['mvt'] == 'ii'
def is_third(piece): return piece['mvt'] == 'iii'


# find function
def get_piece(db, CAT, mvt): return [piece for piece in db if piece['CAT'] == CAT and piece['mvt'] == mvt][0]


