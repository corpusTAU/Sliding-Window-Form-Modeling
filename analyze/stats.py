"""
For reporting auxiliary stats on the data, such as pitch classes present in the DB.
"""


from utils import int_to_pitch
from prepare_pieces import import_db, db_name


def get_used_PC_stats(db):
    used_PCs = {}
    
    for piece in db:
        for pc in range(piece.min_key, piece.max_key + 1):
            used_PCs[pc] = used_PCs.get(pc, 0) + 1
    
    import matplotlib.pyplot as plt
    
    plt.rcParams['savefig.dpi'] = 800
    fig, ax = plt.subplots()
    
    ax.barh(list(used_PCs.keys()), list(used_PCs.values()), align='center')
    ax.set_yticks(list(used_PCs.keys()))
    ax.set_yticklabels([int_to_pitch(PC) for PC in used_PCs.keys()])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlim([0,len(db)])
    ax.set_ylim([min(used_PCs.keys())-0.4, max(used_PCs.keys())+0.4])
    
    plt.show()



if __name__ == "__main__":
    db = import_db(db_name(num_windows=9, window_size=0.2))
    db_M = [p for p in db if p.composer == "Mozart"]
    db_B = [p for p in db if p.composer == "Beethoven"]
    get_used_PC_stats(db)
    