"""

This module contains functions for loading the preprocessed databses,
performing the analyses described in the paper, and generating the visualizations.
See the bottom for usage examples.

"""



from prepare_pieces import import_db, db_name, preprocess_db
from visualize.PCA import (PCA_3d_figure,
                           color_by_composer, color_by_form_category,
                           marker_by_form_category, marker_by_composer)
from visualize.pitch_class_weights import visualize_window_vector


#### PCA dimension reduction

def attach_PCA(db, num_components=2):
    from sklearn.decomposition import PCA
    samples = [piece.features for piece in db]
    pca = PCA(n_components = num_components)
    pca_vectors = pca.fit_transform(samples)
    
    attr_name = "PCA_{}d".format(num_components)
    
    for i in range(len(db)):
        setattr(db[i], attr_name, pca_vectors[i])
    
    return pca


#### visualizations

def PCA_3d_visualization():
    # change num_windows and window_size to load any of the available preprocessed databases
    db = import_db(db_name(num_windows=90, window_size=0.1))
    
    attach_PCA(db, num_components=3)
    
    db = [piece for piece in db if piece.form_category != "Misc"] # filter out Misc movementss
    
    PCA_3d_figure(db,
                  markers=marker_by_form_category, #marker_by_composer
                  coloring=color_by_form_category, #color_by_composer
                  is_annotate=False)
    



def plot_PC_weight_by_form():
    """
    shows the "average" weight of each peach class along the time axis for each form category
    """
    
    db = import_db(db_name(num_windows=90, window_size=0.1))
    
    min_key = min([piece.min_key for piece in db])
    max_key = max([piece.max_key for piece in db])
    
    db_ = [piece for piece in db if piece.form_category == "Sonata"]
    avg = [sum([piece.features[i] for piece in db_])/len(db_) for i in range(len(db_[0].features))]
    visualize_window_vector(avg, min_key, max_key, title="Sonata")
    
    db_ = [piece for piece in db if piece.form_category == "ABA"]
    avg = [sum([piece.features[i] for piece in db_])/len(db_) for i in range(len(db_[0].features))]
    visualize_window_vector(avg, min_key, max_key, title="ABA")
    
    db_ = [piece for piece in db if piece.form_category == "Variations"]
    avg = [sum([piece.features[i] for piece in db_])/len(db_) for i in range(len(db_[0].features))]
    visualize_window_vector(avg, min_key, max_key, title="Variations")


    




#### confusion tables & evaluation

def print_confusion_matrix(matrix, rows):
    # for 3x3 matrix
    print(f"  | {rows[0]}  | {rows[1]}  | {rows[2]}")
    print(f"--+----+----+---")
    print(f"{rows[0]} | {matrix[0][0]: <2} | {matrix[0][1]: <2} | {matrix[0][2]: <2}")
    print(f"{rows[1]} | {matrix[1][0]: <2} | {matrix[1][1]: <2} | {matrix[1][2]: <2}")
    print(f"{rows[2]} | {matrix[2][0]: <2} | {matrix[2][1]: <2} | {matrix[2][2]: <2}")


def confusion_success(confusion_matrix):
    # computes rate of correct prediction given a matrix
    main_diagonal_sum = sum([confusion_matrix[i][i] for i in range(len(confusion_matrix))])
    total_sum = sum([sum(confusion_matrix[i]) for i in range(len(confusion_matrix))])
    return main_diagonal_sum/total_sum



#### SVM

def SVM_once(db, num_dims=12, is_PCA=True, report_error=False):
    from sklearn.svm import SVC
    
    classes_key = {"Sonata":0, "ABA":1, "Variations":2}
    confusion = [[0 for ii in range(len(classes_key))] for i in range(len(classes_key))]
    
    for i in range(len(db)):
        if db[i].form_category == "Misc":
            continue
        
        db_ = [db[ii] for ii in range(len(db)) if ii != i and db[ii].form_category != "Misc"] # leave one out
        
        if is_PCA:
            pca = attach_PCA(db_, num_components=num_dims)
        
        x_feature = f"PCA_{num_dims}d" if is_PCA else "features"
        x_train = [getattr(piece, x_feature) for piece in db_]
        y_train = [piece.form_category for piece in db_]
        
        x_test = pca.transform([db[i].features])[0] if is_PCA else getattr(db[i], x_feature)
        y_test = db[i].form_category
        
        cl = SVC(kernel="rbf", C=4).fit(x_train, y_train)
        prediction = cl.predict([x_test])
        
        confusion[classes_key[prediction[0]]][classes_key[y_test]] += 1
        
        if report_error and prediction != y_test:
            print(f"{db[i].title_tonality}: Predicted {prediction[0]}, should be {y_test}.")
        
    print_confusion_matrix(confusion, "SAV")
    print("Success rate: {}%".format(round(confusion_success(confusion)*100)))
    
def SVM_classify():
    
    params = ((90, 0.1), (30, 0.1), (18, 0.1),
              (58, 0.15), (20, 0.15), (12, 0.15),
              (40, 0.2), (15, 0.2), (9, 0.2))
    
    num_dims = 26
    
    print("\nStatic baseline:")
    db = import_db(db_name(num_windows=1, window_size=1))
    SVM_once(db, num_dims=num_dims, is_PCA=False)
    
    for p in params:
        print(f"\nnum. windows: {p[0]}; window size: {p[1]*100}%")
        db = import_db(db_name(num_windows=p[0], window_size=p[1]))
        # report misclassifications in detail only for one parameter setting
        SVM_once(db, num_dims=num_dims, report_error=p[0] == 90)
        
    

    
#### ANNs

def ANN_once(db, num_dims=26, is_PCA=True, report_error=False):
    from sklearn.neural_network import MLPClassifier
    
    classes_key = {"Sonata":0, "ABA":1, "Variations":2}
    
    confusion = [[0 for ii in range(len(classes_key))] for i in range(len(classes_key))]
    
    for i in range(len(db)):
        if db[i].form_category == "Misc":
            continue
        
        db_ = [db[ii] for ii in range(len(db)) if ii != i and db[ii].form_category != "Misc"] # leave one out
        
        if is_PCA:
            pca = attach_PCA(db_, num_components=num_dims)
        
        x_feature = f"PCA_{num_dims}d" if is_PCA else "features"
        x_train = [getattr(piece, x_feature) for piece in db_]
        y_train = [piece.form_category for piece in db_]
        
        x_test = pca.transform([db[i].features])[0] if is_PCA else getattr(db[i], x_feature)
        y_test = db[i].form_category
        
        
        
        
        clf = MLPClassifier(hidden_layer_sizes=8,
                            random_state=1,
                            solver='lbfgs',
                            learning_rate_init=0.0002,
                            max_iter=10000).fit(x_train, y_train)
        
        prediction = clf.predict([x_test])
        
        confusion[classes_key[prediction[0]]][classes_key[y_test]] += 1
        
        if report_error and prediction != y_test:
            print(f"{db[i].title_tonality}: Predicted {prediction[0]}, should be {y_test}.")
        
    print_confusion_matrix(confusion, "SAV")
    print("Success rate: {}%".format(round(confusion_success(confusion)*100)))


def ANN_classify():
    
    params = ((90, 0.1), (30, 0.1), (18, 0.1),
              (58, 0.15), (20, 0.15), (12, 0.15),
              (40, 0.2), (15, 0.2), (9, 0.2))
    
    num_dims = 26
    
    print("\nStatic baseline:")
    db = import_db(db_name(num_windows=1, window_size=1))
    ANN_once(db, num_dims=num_dims, is_PCA=False)
    
    for p in params:
        print(f"\nnum. windows: {p[0]}; window size: {p[1]*100}%")
        db = import_db(db_name(num_windows=p[0], window_size=p[1]))
        # report misclassifications in detail only for one parameter setting
        ANN_once(db, num_dims=num_dims)

#### GMM


def evaluate_GMM_results(db, prediction):
    perms = (("Sonata", "ABA", "Variations"), ("Sonata", "Variations", "ABA"),
             ("ABA", "Sonata", "Variations"), ("ABA", "Variations", "Sonata"),
             ("Variations", "Sonata", "ABA"), ("Variations", "ABA", "Sonata"))
    
    accuracy_rates = []
    
    for perm in perms:
        acc = 0
        
        for i in range(len(db)):
            if perm[prediction[i]] == db[i].form_category:
                acc += 1
        
        accuracy_rates.append(acc / len(db) * 100)
    
    return max(accuracy_rates)

def GMM_once(db, feature, num_components, is_print=True):
    from sklearn.mixture import GaussianMixture
    samples = [getattr(piece, feature) for piece in db]
    
    gmm = GaussianMixture(n_components=num_components, random_state=None).fit(samples)
    y_pred = gmm.predict(samples)
    
    if not is_print:
        return y_pred
    
    for i in range(num_components):
        print(f"\nCategory {i+1}:")
        for ii in range(len(db)):
            if y_pred[ii] == i:
                print(f"{db[ii].title} - {db[ii].form_category} ({db[ii].form})")
  
def GMM_clustering(num_dims=3, num_iterations=10, num_windows=90, window_size=0.1):
    print(f"Testing GMMs for PCA dim: {num_dims}, over {num_iterations} iterations, {num_windows} windows of size {window_size*100:0.0f}%")
    db = import_db(db_name(num_windows=num_windows, window_size=window_size))
    attach_PCA(db, num_components=num_dims)
    db = [piece for piece in db if piece.form_category not in ("Misc")]
    
    best_scores = []
    
    for i in range(num_iterations):
        predictions = GMM_once(db, feature=f"PCA_{num_dims}d", num_components=3, is_print=False)
        best_scores.append(evaluate_GMM_results(db, predictions))
    
    print(f"Sample scores: {best_scores[:12]}")
    print(f"Avg. best score: {sum(best_scores)/num_iterations:0.1f}%")
    print(f"Range: {min(best_scores):0.1f}% - {max(best_scores):0.1f}%")
    

#### preprocessing

def export_dbs():
    """
    Preprocessing on the db according to the nine configurations
    discussed in the paper, as well as the whole-piece histogram analysis.
    Results are output into *.p files, which can then be imported and analyzed.
    """
    return # manual lock due to time-consuming process
    # window size = 10%
    preprocess_db(90, 0.1) # overlap = ~90%
    preprocess_db(30, 0.1) # overlap = ~70%
    preprocess_db(18, 0.1) # overlap = ~50%
    
    # window size = 15%
    preprocess_db(58, 0.15) # overlap = ~90%
    preprocess_db(20, 0.15) # overlap = ~70%
    preprocess_db(12, 0.15) # overlap = ~50%
    
    # window size = 20%
    preprocess_db(40, 0.2) # overlap = ~90%
    preprocess_db(15, 0.2) # overlap = ~70%
    preprocess_db(9 , 0.2) # overlap = ~50%
    
    # whole-piece histogram
    preprocess_db(1, 1)



if __name__ == "__main__":
    
    # uncomment any of these
    
    
    ## supervised classification
    #SVM_classify()
    #ANN_classify()
    
    
    ## unsupervised clustering
    
    # sliding-window histograms
    #GMM_clustering(num_dims=3, num_iterations=100, num_windows=58, window_size=0.15)
    # whole-piece histograms
    #GMM_clustering(num_dims=3, num_iterations=100, num_windows=1, window_size=1)
    
    ## visualizations
    
    #PCA_3d_visualization()
    #plot_PC_weight_by_form()
    
    ...
    















