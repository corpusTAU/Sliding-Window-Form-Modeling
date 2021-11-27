## Sliding-Window Pitch-Class Histograms as a Means of Modeling Musical Form
This is supplementary code for the [TISMIR](https://transactions.ismir.net/) paper
[Sliding-Window Pitch-Class Histograms as a Means of Modeling Musical Form](https://doi.org/10.5334/tismir.83),


This repository contains the following:
* Preprocessing code (`process/*`, `analyze/prepare_pieces.py`), which reads MusicXML files and produces
sliding-window pitch-class histogram vectors, as described in the paper.
The data itslef is not included; it consists of Mozart's piano sonata movements
as obtained from [DCML](https://github.com/DCMLab/mozart_piano_sonatas), with minor adjustments detailed in the paper,
as well as Beethoven's piano sonata movements, adapted from [musescore.com](https://musescore.com/user/19710/sets/54311).

* Preprocessed binary databases for the nine configurations of hyper-parameters described in the paper,
as well as for the static histogram configuraion (`db/*.p`).
These are the exact outputs of the preprocessing code over the dataset as described in the paper.

* Metadata for all movements in the dataset, including detailed form labels (`metadata/*`).

* Analysis functionality, applying SVM and ANN classification, and GMM clustering (`analyze/analyze.py`).

* Visualization and basic dataset statistics (`visualize/*`, `analyze/analyze.py`, `analyze/stats.py`).

The main entry point is `analyze/analyze.py`, which includes at the bottom commented
calls to the analyses presented in the paper, and also to the code
generating most of the figures. To perform analysis, uncomment any of these and run.

A separate entry pont, `analyze/stats.py`, is used for analyzing the various pitch classes
appearing across the corpus.

## Dependencies
The code requires Python 3 (probably >= 3.6 would suffice)
with the following libraries installed:
* [music21](https://github.com/cuthbertLab/music21) (for preprocessing)
* SciPy (including `scikit-learn` and `matplotlib`) (for analysis and visualization)




