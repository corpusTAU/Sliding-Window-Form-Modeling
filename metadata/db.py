"""
The pieces in our corpus were annotated using 21 unique labels, representing
detailed subcategories of formal layouts.

These are mapped onto three generic form labels: Sonata, ABA and Variations.
The remaining subcategories listed below under "Misc." are not included in our analysis.
    
Sonata:
 - Sonata
 - Sonata_with_intro
 - Slow_sonata
 - Sonata_rondo
 - Slow_sonatina
 - 9_part_rondo
 - 2_tempo_sonata
 - 5_part_sonata_rondo

ABA:
 - Minuet&Trio
 - Slow_ABA
 - Rondo_ABA
 - Scherzo&Trio
 - Minuet/Scherzo&Trio

Variations:
 - Variations

Misc. (labels not included in the analysis):
 - 5_part_rondo
 - Binary_varied_repeats
 - Reigen_rondo
 - Fugue_with_intro
 - Free_cantilena
 - Rounded_binary
 - 7_part_rondo
"""

from metadata.db_util import is_major


xml_path = "data/"

Mozart_path = xml_path + "Mozart_piano_sonatas/"
Beethoven_path = xml_path + "Beethoven_piano_sonatas/"


Mozart_sonatas = [
    {'filename':'Moz_K279-1.xml', 'CAT':'279', 'mvt':'i', 'tonality':'C', 'form':'Sonata'},
    {'filename':'Moz_K279-2.xml', 'CAT':'279', 'mvt':'ii', 'tonality':'F', 'form':'Slow_sonata'},
    {'filename':'Moz_K279-3.xml', 'CAT':'279', 'mvt':'iii', 'tonality':'C', 'form':'Sonata'},
    
    {'filename':'Moz_K280-1.xml', 'CAT':'280', 'mvt':'i', 'tonality':'F', 'form':'Sonata'},
    {'filename':'Moz_K280-2.xml', 'CAT':'280', 'mvt':'ii', 'tonality':'f', 'form':'Slow_sonata'},
    {'filename':'Moz_K280-3.xml', 'CAT':'280', 'mvt':'iii', 'tonality':'F', 'form':'Sonata'},
    
    {'filename':'Moz_K281-1.xml', 'CAT':'281', 'mvt':'i', 'tonality':'Bb', 'form':'Sonata'},
    {'filename':'Moz_K281-2.xml', 'CAT':'281', 'mvt':'ii', 'tonality':'Eb', 'form':'Slow_sonata'},
    {'filename':'Moz_K281-3.xml', 'CAT':'281', 'mvt':'iii', 'tonality':'Bb', 'form':'9_part_rondo'},
    
    {'filename':'Moz_K282-1.xml', 'CAT':'282', 'mvt':'i', 'tonality':'Eb', 'form':'Slow_sonata'},
    {'filename':'Moz_K282-2.xml', 'CAT':'282', 'mvt':'ii', 'tonality':'Bb', 'form':'Minuet&Trio'},
    {'filename':'Moz_K282-3.xml', 'CAT':'282', 'mvt':'iii', 'tonality':'Eb', 'form':'Sonata'},
    
    {'filename':'Moz_K283-1.xml', 'CAT':'283', 'mvt':'i', 'tonality':'G', 'form':'Sonata'},
    {'filename':'Moz_K283-2.xml', 'CAT':'283', 'mvt':'ii', 'tonality':'C', 'form':'Slow_sonata'},
    {'filename':'Moz_K283-3.xml', 'CAT':'283', 'mvt':'iii', 'tonality':'G', 'form':'Sonata'},
    
    {'filename':'Moz_K284-1.xml', 'CAT':'284', 'mvt':'i', 'tonality':'D', 'form':'Sonata'},
    {'filename':'Moz_K284-2.xml', 'CAT':'284', 'mvt':'ii', 'tonality':'A', 'form':'5_part_rondo'},
    {'filename':'Moz_K284-3.xml', 'CAT':'284', 'mvt':'iii', 'tonality':'D', 'form':'Variations'},
    
    {'filename':'Moz_K309-1.xml', 'CAT':'309', 'mvt':'i', 'tonality':'C', 'form':'Sonata'},
    {'filename':'Moz_K309-2.xml', 'CAT':'309', 'mvt':'ii', 'tonality':'F', 'form':'Binary_varied_repeats'},
    {'filename':'Moz_K309-3.xml', 'CAT':'309', 'mvt':'iii', 'tonality':'C', 'form':'Sonata_rondo'},
    
    {'filename':'Moz_K310-1.xml', 'CAT':'310', 'mvt':'i', 'tonality':'a', 'form':'Sonata'},
    {'filename':'Moz_K310-2.xml', 'CAT':'310', 'mvt':'ii', 'tonality':'F', 'form':'Slow_sonata'},
    {'filename':'Moz_K310-3.xml', 'CAT':'310', 'mvt':'iii', 'tonality':'a', 'form':'Sonata_rondo'},
    
    {'filename':'Moz_K311-1.xml', 'CAT':'311', 'mvt':'i', 'tonality':'D', 'form':'Sonata'},
    {'filename':'Moz_K311-2.xml', 'CAT':'311', 'mvt':'ii', 'tonality':'G', 'form':'Slow_sonatina'},
    {'filename':'Moz_K311-3.xml', 'CAT':'311', 'mvt':'iii', 'tonality':'D', 'form':'Sonata_rondo'},
    
    {'filename':'Moz_K330-1.xml', 'CAT':'330', 'mvt':'i', 'tonality':'C', 'form':'Sonata'}, 
    {'filename':'Moz_K330-2.xml', 'CAT':'330', 'mvt':'ii', 'tonality':'F', 'form':'Slow_ABA'},
    {'filename':'Moz_K330-3.xml', 'CAT':'330', 'mvt':'iii', 'tonality':'C', 'form':'Sonata'}, 
    
    {'filename':'Moz_K331-1.xml', 'CAT':'331', 'mvt':'i', 'tonality':'A', 'form':'Variations'},
    {'filename':'Moz_K331-2.xml', 'CAT':'331', 'mvt':'ii', 'tonality':'A', 'form':'Minuet&Trio'},
    {'filename':'Moz_K331-3.xml', 'CAT':'331', 'mvt':'iii', 'tonality':'a', 'form':'Rondo_ABA'},
    
    {'filename':'Moz_K332-1.xml', 'CAT':'332', 'mvt':'i', 'tonality':'F', 'form':'Sonata'},
    {'filename':'Moz_K332-2.xml', 'CAT':'332', 'mvt':'ii', 'tonality':'Bb', 'form':'Slow_sonatina'},
    {'filename':'Moz_K332-3.xml', 'CAT':'332', 'mvt':'iii', 'tonality':'F', 'form':'Sonata'},
    
    {'filename':'Moz_K333-1.xml', 'CAT':'333', 'mvt':'i', 'tonality':'Bb', 'form':'Sonata'},
    {'filename':'Moz_K333-2.xml', 'CAT':'333', 'mvt':'ii', 'tonality':'Eb', 'form':'Slow_sonata'},
    {'filename':'Moz_K333-3.xml', 'CAT':'333', 'mvt':'iii', 'tonality':'Bb', 'form':'Sonata_rondo'},
    
    {'filename':'Moz_K457-1.xml', 'CAT':'457', 'mvt':'i', 'tonality':'c', 'form':'Sonata'},
    {'filename':'Moz_K457-2.xml', 'CAT':'457', 'mvt':'ii', 'tonality':'Eb', 'form':'5_part_rondo'},
    {'filename':'Moz_K457-3.xml', 'CAT':'457', 'mvt':'iii', 'tonality':'c', 'form':'Sonata_rondo'},

    {'filename':'Moz_K533-1.xml', 'CAT':'533', 'mvt':'i', 'tonality':'F', 'form':'Sonata'},
    {'filename':'Moz_K533-2.xml', 'CAT':'533', 'mvt':'ii', 'tonality':'Bb', 'form':'Slow_sonata'},
    {'filename':'Moz_K533-3.xml', 'CAT':'533', 'mvt':'iii', 'tonality':'F', 'form':'9_part_rondo'},
    
    {'filename':'Moz_K545-1.xml', 'CAT':'545', 'mvt':'i', 'tonality':'C', 'form':'Sonata'},
    {'filename':'Moz_K545-2.xml', 'CAT':'545', 'mvt':'ii', 'tonality':'G', 'form':'Slow_ABA'},
    {'filename':'Moz_K545-3.xml', 'CAT':'545', 'mvt':'iii', 'tonality':'C', 'form':'5_part_rondo'},
    
    {'filename':'Moz_K570-1.xml', 'CAT':'570', 'mvt':'i', 'tonality':'Bb', 'form':'Sonata'},
    {'filename':'Moz_K570-2.xml', 'CAT':'570', 'mvt':'ii', 'tonality':'Eb', 'form':'5_part_rondo'},
    {'filename':'Moz_K570-3.xml', 'CAT':'570', 'mvt':'iii', 'tonality':'Bb', 'form':'Reigen_rondo'},
    
    {'filename':'Moz_K576-1.xml', 'CAT':'576', 'mvt':'i', 'tonality':'D', 'form':'Sonata'},
    {'filename':'Moz_K576-2.xml', 'CAT':'576', 'mvt':'ii', 'tonality':'A', 'form':'Slow_ABA'},
    {'filename':'Moz_K576-3.xml', 'CAT':'576', 'mvt':'iii', 'tonality':'D', 'form':'Sonata_rondo'},
    ]

for p in Mozart_sonatas:
    p["composer"] = "Mozart"
    p["filename"] = Mozart_path + p["filename"]
    
    








###################################

Beethoven_sonatas = [
    {'filename':'Bee_PS01-1.xml', 'CAT':'1', 'mvt':'i', 'tonality':'f', 'form':'Sonata'},
    {'filename':'Bee_PS01-2.xml', 'CAT':'1', 'mvt':'ii', 'tonality':'F', 'form':'Slow_sonatina'},
    {'filename':'Bee_PS01-3.xml', 'CAT':'1', 'mvt':'iii', 'tonality':'f', 'form':'Minuet&Trio'},
    {'filename':'Bee_PS01-4.xml', 'CAT':'1', 'mvt':'iv', 'tonality':'f', 'form':'Sonata'},

    {'filename':'Bee_PS02-1.xml', 'CAT':'2', 'mvt':'i', 'tonality':'A', 'form':'Sonata'},
    {'filename':'Bee_PS02-2.xml', 'CAT':'2', 'mvt':'ii', 'tonality':'D', 'form':'Slow_ABA'},
    {'filename':'Bee_PS02-3.xml', 'CAT':'2', 'mvt':'iii', 'tonality':'A', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS02-4.xml', 'CAT':'2', 'mvt':'iv', 'tonality':'A', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS03-1.xml', 'CAT':'3', 'mvt':'i', 'tonality':'C', 'form':'Sonata'},
    {'filename':'Bee_PS03-2.xml', 'CAT':'3', 'mvt':'ii', 'tonality':'E', 'form':'Slow_ABA'},
    {'filename':'Bee_PS03-3.xml', 'CAT':'3', 'mvt':'iii', 'tonality':'C', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS03-4.xml', 'CAT':'3', 'mvt':'iv', 'tonality':'C', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS04-1.xml', 'CAT':'4', 'mvt':'i', 'tonality':'Eb', 'form':'Sonata'},
    {'filename':'Bee_PS04-2.xml', 'CAT':'4', 'mvt':'ii', 'tonality':'C', 'form':'Slow_ABA'},
    {'filename':'Bee_PS04-3.xml', 'CAT':'4', 'mvt':'iii', 'tonality':'Eb', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS04-4.xml', 'CAT':'4', 'mvt':'iv', 'tonality':'Eb', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS05-1.xml', 'CAT':'5', 'mvt':'i', 'tonality':'c', 'form':'Sonata'},
    {'filename':'Bee_PS05-2.xml', 'CAT':'5', 'mvt':'ii', 'tonality':'Ab', 'form':'Slow_sonatina'},
    {'filename':'Bee_PS05-3.xml', 'CAT':'5', 'mvt':'iii', 'tonality':'c', 'form':'Sonata'},

    {'filename':'Bee_PS06-1.xml', 'CAT':'6', 'mvt':'i', 'tonality':'F', 'form':'Sonata'},
    {'filename':'Bee_PS06-2.xml', 'CAT':'6', 'mvt':'ii', 'tonality':'f', 'form':'Minuet/Scherzo&Trio'},
    {'filename':'Bee_PS06-3.xml', 'CAT':'6', 'mvt':'iii', 'tonality':'F', 'form':'Sonata'},

    {'filename':'Bee_PS07-1.xml', 'CAT':'7', 'mvt':'i', 'tonality':'D', 'form':'Sonata'},
    {'filename':'Bee_PS07-2.xml', 'CAT':'7', 'mvt':'ii', 'tonality':'d', 'form':'Slow_sonata'},
    {'filename':'Bee_PS07-3.xml', 'CAT':'7', 'mvt':'iii', 'tonality':'D', 'form':'Minuet&Trio'},
    {'filename':'Bee_PS07-4.xml', 'CAT':'7', 'mvt':'iv', 'tonality':'D', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS08-1.xml', 'CAT':'8', 'mvt':'i', 'tonality':'c', 'form':'Sonata_with_intro'},
    {'filename':'Bee_PS08-2.xml', 'CAT':'8', 'mvt':'ii', 'tonality':'Ab', 'form':'5_part_rondo'},
    {'filename':'Bee_PS08-3.xml', 'CAT':'8', 'mvt':'iii', 'tonality':'c', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS09-1.xml', 'CAT':'9', 'mvt':'i', 'tonality':'E', 'form':'Sonata'},
    {'filename':'Bee_PS09-2.xml', 'CAT':'9', 'mvt':'ii', 'tonality':'e', 'form':'Slow_ABA'},
    {'filename':'Bee_PS09-3.xml', 'CAT':'9', 'mvt':'iii', 'tonality':'E', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS10-1.xml', 'CAT':'10', 'mvt':'i', 'tonality':'G', 'form':'Sonata'},
    {'filename':'Bee_PS10-2.xml', 'CAT':'10', 'mvt':'ii', 'tonality':'C', 'form':'Variations'},
    {'filename':'Bee_PS10-3.xml', 'CAT':'10', 'mvt':'iii', 'tonality':'G', 'form':'5_part_rondo'},

    {'filename':'Bee_PS11-1.xml', 'CAT':'11', 'mvt':'i', 'tonality':'Bb', 'form':'Sonata'},
    {'filename':'Bee_PS11-2.xml', 'CAT':'11', 'mvt':'ii', 'tonality':'Eb', 'form':'Slow_sonata'},
    {'filename':'Bee_PS11-3.xml', 'CAT':'11', 'mvt':'iii', 'tonality':'Bb', 'form':'Minuet&Trio'},
    {'filename':'Bee_PS11-4.xml', 'CAT':'11', 'mvt':'iv', 'tonality':'Bb', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS12-1.xml', 'CAT':'12', 'mvt':'i', 'tonality':'Ab', 'form':'Variations'},
    {'filename':'Bee_PS12-2.xml', 'CAT':'12', 'mvt':'ii', 'tonality':'Ab', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS12-3.xml', 'CAT':'12', 'mvt':'iii', 'tonality':'ab', 'form':'Slow_ABA'},
    {'filename':'Bee_PS12-4.xml', 'CAT':'12', 'mvt':'iv', 'tonality':'Ab', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS13-1.xml', 'CAT':'13', 'mvt':'i', 'tonality':'Eb', 'form':'5_part_rondo'},
    {'filename':'Bee_PS13-2.xml', 'CAT':'13', 'mvt':'ii', 'tonality':'c', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS13-3.xml', 'CAT':'13', 'mvt':'iii', 'tonality':'Ab', 'form':'Free_cantilena'},
    {'filename':'Bee_PS13-4.xml', 'CAT':'13', 'mvt':'iv', 'tonality':'Eb', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS14-1.xml', 'CAT':'14', 'mvt':'i', 'tonality':'c#', 'form':'Free_cantilena'},
    {'filename':'Bee_PS14-2.xml', 'CAT':'14', 'mvt':'ii', 'tonality':'Db', 'form':'Minuet/Scherzo&Trio'},
    {'filename':'Bee_PS14-3.xml', 'CAT':'14', 'mvt':'iii', 'tonality':'c#', 'form':'Sonata'},

    {'filename':'Bee_PS15-1.xml', 'CAT':'15', 'mvt':'i', 'tonality':'D', 'form':'Sonata'},
    {'filename':'Bee_PS15-2.xml', 'CAT':'15', 'mvt':'ii', 'tonality':'d', 'form':'Slow_ABA'},
    {'filename':'Bee_PS15-3.xml', 'CAT':'15', 'mvt':'iii', 'tonality':'D', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS15-4.xml', 'CAT':'15', 'mvt':'iv', 'tonality':'D', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS16-1.xml', 'CAT':'16', 'mvt':'i', 'tonality':'G', 'form':'Sonata'},
    {'filename':'Bee_PS16-2.xml', 'CAT':'16', 'mvt':'ii', 'tonality':'C', 'form':'Slow_ABA'},
    {'filename':'Bee_PS16-3.xml', 'CAT':'16', 'mvt':'iii', 'tonality':'G', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS17-1.xml', 'CAT':'17', 'mvt':'i', 'tonality':'d', 'form':'Sonata'},
    {'filename':'Bee_PS17-2.xml', 'CAT':'17', 'mvt':'ii', 'tonality':'Bb', 'form':'Slow_sonatina'},
    {'filename':'Bee_PS17-3.xml', 'CAT':'17', 'mvt':'iii', 'tonality':'d', 'form':'Sonata'},

    {'filename':'Bee_PS18-1.xml', 'CAT':'18', 'mvt':'i', 'tonality':'Eb', 'form':'Sonata'},
    {'filename':'Bee_PS18-2.xml', 'CAT':'18', 'mvt':'ii', 'tonality':'Ab', 'form':'Slow_sonata'},
    {'filename':'Bee_PS18-3.xml', 'CAT':'18', 'mvt':'iii', 'tonality':'Eb', 'form':'Minuet&Trio'},
    {'filename':'Bee_PS18-4.xml', 'CAT':'18', 'mvt':'iv', 'tonality':'Eb', 'form':'Sonata'},

    {'filename':'Bee_PS19-1.xml', 'CAT':'19', 'mvt':'i', 'tonality':'g', 'form':'Sonata'},
    {'filename':'Bee_PS19-2.xml', 'CAT':'19', 'mvt':'ii', 'tonality':'G', 'form':'5_part_sonata_rondo'},

    {'filename':'Bee_PS20-1.xml', 'CAT':'20', 'mvt':'i', 'tonality':'G', 'form':'Sonata'},
    {'filename':'Bee_PS20-2.xml', 'CAT':'20', 'mvt':'ii', 'tonality':'G', 'form':'5_part_rondo'},

    {'filename':'Bee_PS21-1.xml', 'CAT':'21', 'mvt':'i', 'tonality':'C', 'form':'Sonata'},
    {'filename':'Bee_PS21-2.xml', 'CAT':'21', 'mvt':'ii', 'tonality':'F', 'form':'Free_cantilena'},
    {'filename':'Bee_PS21-3.xml', 'CAT':'21', 'mvt':'iii', 'tonality':'C', 'form':'5_part_rondo'},

    {'filename':'Bee_PS22-1.xml', 'CAT':'22', 'mvt':'i', 'tonality':'F', 'form':'5_part_rondo'},
    {'filename':'Bee_PS22-2.xml', 'CAT':'22', 'mvt':'ii', 'tonality':'F', 'form':'Rounded_binary'},

    {'filename':'Bee_PS23-1.xml', 'CAT':'23', 'mvt':'i', 'tonality':'f', 'form':'Sonata'},
    {'filename':'Bee_PS23-2.xml', 'CAT':'23', 'mvt':'ii', 'tonality':'Db', 'form':'Variations'},
    {'filename':'Bee_PS23-3.xml', 'CAT':'23', 'mvt':'iii', 'tonality':'f', 'form':'Sonata'},

    {'filename':'Bee_PS24-1.xml', 'CAT':'24', 'mvt':'i', 'tonality':'F#', 'form':'Sonata_with_intro'},
    {'filename':'Bee_PS24-2.xml', 'CAT':'24', 'mvt':'ii', 'tonality':'F#', 'form':'7_part_rondo'},

    {'filename':'Bee_PS25-1.xml', 'CAT':'25', 'mvt':'i', 'tonality':'G', 'form':'Sonata'},
    {'filename':'Bee_PS25-2.xml', 'CAT':'25', 'mvt':'ii', 'tonality':'g', 'form':'Slow_ABA'},
    {'filename':'Bee_PS25-3.xml', 'CAT':'25', 'mvt':'iii', 'tonality':'G', 'form':'5_part_rondo'},

    {'filename':'Bee_PS26-1.xml', 'CAT':'26', 'mvt':'i', 'tonality':'Eb', 'form':'Sonata_with_intro'},
    {'filename':'Bee_PS26-2.xml', 'CAT':'26', 'mvt':'ii', 'tonality':'c', 'form':'Free_cantilena'},
    {'filename':'Bee_PS26-3.xml', 'CAT':'26', 'mvt':'iii', 'tonality':'Eb', 'form':'Sonata'},

    {'filename':'Bee_PS27-1.xml', 'CAT':'27', 'mvt':'i', 'tonality':'e', 'form':'Sonata'},
    {'filename':'Bee_PS27-2.xml', 'CAT':'27', 'mvt':'ii', 'tonality':'E', 'form':'Sonata_rondo'},

    {'filename':'Bee_PS28-1.xml', 'CAT':'28', 'mvt':'i', 'tonality':'A', 'form':'Slow_sonata'},
    {'filename':'Bee_PS28-2.xml', 'CAT':'28', 'mvt':'ii', 'tonality':'F', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS28-3.xml', 'CAT':'28', 'mvt':'iii', 'tonality':'a', 'form':'Free_cantilena'},
    {'filename':'Bee_PS28-4.xml', 'CAT':'28', 'mvt':'iv', 'tonality':'A', 'form':'Sonata'},

    {'filename':'Bee_PS29-1.xml', 'CAT':'29', 'mvt':'i', 'tonality':'Bb', 'form':'Sonata'},
    {'filename':'Bee_PS29-2.xml', 'CAT':'29', 'mvt':'ii', 'tonality':'Bb', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS29-3.xml', 'CAT':'29', 'mvt':'iii', 'tonality':'f#', 'form':'Slow_sonata'},
    {'filename':'Bee_PS29-4.xml', 'CAT':'29', 'mvt':'iv', 'tonality':'Bb', 'form':'Fugue_with_intro'},

    {'filename':'Bee_PS30-1.xml', 'CAT':'30', 'mvt':'i', 'tonality':'E', 'form':'2_tempo_sonata'},
    {'filename':'Bee_PS30-2.xml', 'CAT':'30', 'mvt':'ii', 'tonality':'e', 'form':'Sonata'},
    {'filename':'Bee_PS30-3.xml', 'CAT':'30', 'mvt':'iii', 'tonality':'E', 'form':'Variations'},

    {'filename':'Bee_PS31-1.xml', 'CAT':'31', 'mvt':'i', 'tonality':'Ab', 'form':'Slow_sonata'},
    {'filename':'Bee_PS31-2.xml', 'CAT':'31', 'mvt':'ii', 'tonality':'f', 'form':'Scherzo&Trio'},
    {'filename':'Bee_PS31-3.xml', 'CAT':'31', 'mvt':'iii', 'tonality':'Ab', 'form':'Fugue_with_intro'},

    {'filename':'Bee_PS32-1.xml', 'CAT':'32', 'mvt':'i', 'tonality':'c', 'form':'Sonata_with_intro'},
    {'filename':'Bee_PS32-2.xml', 'CAT':'32', 'mvt':'ii', 'tonality':'C', 'form':'Variations'},
    ]

for p in Beethoven_sonatas:
    p["filename"] = Beethoven_path + p["filename"]
    p["composer"] = "Beethoven"



###### Various collections for analysis ###########


Mozart_Beethoven_complete = Mozart_sonatas + Beethoven_sonatas
Mozart_Beethoven_major = [piece for piece in Mozart_Beethoven_complete if is_major(piece)]
Mozart_major = [piece for piece in Mozart_sonatas if is_major(piece)]
Beethoven_major = [piece for piece in Beethoven_sonatas if is_major(piece)]





















