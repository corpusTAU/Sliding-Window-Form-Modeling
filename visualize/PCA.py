"""

Visualizing a 3d PCA output, colored by composer or form category.
This expects a loaded and preprocessed database. Usage shown in analyze.py.

"""

#### Helper functions for visualizations

def color_by_composer(piece):
    return {"Mozart": 'red',
            "Beethoven": 'blue'}[piece.composer]

def marker_by_composer(piece):
    return {"Mozart": "d",
            "Beethoven": "x"}[piece.composer]

def color_by_form_category(piece):
    return {"Sonata": 'blue',
            "ABA": 'red',
            "Variations": '#00BB00',
            "Misc": 'grey',
            }[piece.form_category]

def marker_by_form_category(piece):
    return {"Sonata": "x",
            "ABA": "d",
            "Variations": "s",
            "Misc": "-"}[piece.form_category]

####

def PCA_3d_figure(db, is_annotate=False,
                  coloring=None, markers=None,
                  filename=None):
    
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    plt.rcParams['savefig.dpi'] = 800
    fig = plt.figure(figsize=(20,10))
    plt.clf()
    ax = Axes3D(fig)
    
    for i, piece in enumerate(db):
        ax.scatter(piece.PCA_3d[0],
                   piece.PCA_3d[1],
                   piece.PCA_3d[2],
                   c='black' if coloring is None else coloring(piece),
                   marker=None if markers is None else markers(piece))
    
        if is_annotate:
            ax.text(piece.PCA_3d[0],
                    piece.PCA_3d[1],
                    piece.PCA_3d[2],
                    piece.title_tonality, None)
        
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    if filename == None:
        plt.show()
    else:
        fig.savefig(f"output/{filename}.png")
        plt.close(fig)


