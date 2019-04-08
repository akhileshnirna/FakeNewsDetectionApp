import numpy as np
import codecs
import pickle

from collections import OrderedDict as dict
import gensim as g
from gensim.models import Doc2Vec

MODEL_PATH = "./model/saved.model"
FAKE_ACCOUNT_MODE_PATH = 'F_vs_G_model.data'

model = Doc2Vec.load(MODEL_PATH)

print("Gensim Version : {}".format(g.__version__))
print('MODEL LOADED from path : {}'.format(MODEL_PATH))

""" Function converts a set of documents into vectors """
def vectorize(docs):
    vectors = dict()
    for doc_id in docs:
        doc = docs[doc_id]['description']
        input_doc = [doc.lower().strip()]
        v = model.infer_vector(input_doc, alpha=0.01, steps=100)
        vectors[doc_id] = v
    return vectors

""" similarity between 2 vectors computed by the `vectorize` function"""
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.sum(v1 ** 2) ** 1/2) * (np.sum(v2 ** 2) ** 1/2)

""" cluster a set of vectors """
def spectral_cluster(vectors, n_clusters=None):
    from sklearn.cluster import SpectralClustering
    
    # if not provided, n_clusters = min(2, cube_root(num_vectors))
    if not n_clusters:
        n_clusters = int(np.floor(len(vectors) ** 1/3))
        if n_clusters == 0:
            n_clusters = 2
    
    cluster_clf = SpectralClustering(n_clusters=n_clusters, n_jobs=8)
    labels = cluster_clf.fit_predict(vectors)

    return labels

""" perform pca and return an `n dimensional` representation of each vector """
def pca(vectors, n_components=3):
    from sklearn.decomposition import PCA

    pca_dim_reduction = PCA(n_components=n_components)
    pca_dim_reduction.fit(vectors)
    return pca_dim_reduction.transform(vectors)

""" detect fake communities """
def fake_community_detection(docs):
    loaded_model = pickle.load(open(FAKE_ACCOUNT_MODE_PATH, "rb"))
    fake_account_model = loaded_model["classifier"]
    fake_account_scaler = loaded_model["scaler"]    
    
    communities = dict()
    for user_name in docs:
        details = docs[user_name]['details']
        parsed_details = parse_user(details)
        scaled_details = fake_account_scaler.transform(parsed_details.reshape(1, -1))
        fake_probabilty = fake_account_model.predict_proba(scaled_details)
        community_num = docs[user_name]['community']

        if community_num not in communities:
            communities[community_num] = dict()
            communities[community_num]['users'] = []
            communities[community_num]['fake_proba_list'] = []
        
        docs[user_name]['fake_proba'] = fake_probabilty[0][1]
        communities[community_num]['users'].append( docs[user_name] )
        communities[community_num]['fake_proba_list'].append(fake_probabilty[0][1])
    
    for community_num in communities:
        prob = 1
        for p in communities[community_num]['fake_proba_list']:
            prob *= p
        prob ** 1/len(communities[community_num]['fake_proba_list'])
        communities[community_num]['fake_proba'] = prob

    return communities

    

""" Parses user details for prediction """
def parse_user(user_details):
    useful_columns = ["statuses_count", "followers_count", "friends_count", 
        "favourites_count", "listed_count", "default_profile", 
        "profile_banner_url", "profile_background_tile", 
        "profile_background_color" ,"verified"]
    data = []
    for col in useful_columns:
        try:
                val = getattr(user_details, col)
                if isinstance(val, int):
                    data.append(val)
                elif isinstance(val, bool):
                    if val is True:
                        data.append(1)
                    else:
                        data.append(0)
                elif isinstance(val, str):
                    if col == 'profile_banner_url':
                        if val:
                            data.append(1)
                        else:
                            data.append(0)
                    elif col == 'profile_background_color':
                        if val != 'C0DEED':
                            data.append(1)
                        else:
                            data.append(0)
        except:
                data.append(0)
    return np.array(data)
     
