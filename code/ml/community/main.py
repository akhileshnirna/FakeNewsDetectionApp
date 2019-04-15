from collections import OrderedDict as dict
from twitter import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ml.community.api_helper import get_top_friends
from ml.community.graph_helper import generate_graph_from_connections, viz_graph
from ml.community.community import vectorize, spectral_cluster, pca
from ml.community.community import fake_community_detection
from base64 import b64encode
import json
import os
from ml.vars import IMG_PATH, CACHE_PATH

consumer_key = "YrlvTaYmfUFw6C3OnapAKiuaM"
consumer_secret = "QUZXmYYyyugyuT3GMNoOOxtTAst9fbWziGhcNsejDdsDU5tIbL"
access_token = "795922562546970624-6S2XzPe9K2gNrHphl3OUS1tjIgIh8rQ"
access_token_secret = "bfDz7r938dbfdfJai974vcQBeENz32VD8C4eBGZ71OECy"


class CommunityDetectionModel():
    
    def __init__(self):
        self.twitter = Twitter(auth=OAuth(
                access_token,
                access_token_secret,
                consumer_key,
                consumer_secret
                )
        )
    
    def graph_it(self, user_name, num_friends_at_depths=[2, 2], n_clusters=3):
        self.user_name = user_name
        if not os.path.exists(CACHE_PATH):
            connections = get_top_friends(self.twitter, self.user_name, 
                                friends_at_depths=num_friends_at_depths)
            json.dump(connections, open(CACHE_PATH, 'w'))
        else:
            connections = json.load(open(CACHE_PATH, 'r'))
                            
        connection_graph = generate_graph_from_connections(connections)
        viz_graph(connection_graph, save_graph=True, file_name='connections.png')
        # connection_graph = b64encode(open('demo.png', 'rb').read())
        # connection_graph = connection_graph.decode('utf-8')

        docs = self._gen_docs(connections)
        
        description_vectors = vectorize(docs)
        vector_values = list(description_vectors.values())
        
        clustered_labels = spectral_cluster(vector_values, n_clusters=n_clusters)

        for user_name, cluster_label in zip(description_vectors.keys(), clustered_labels):
            docs[user_name]['community'] = str(cluster_label)

        reduced_vectors = pca(vector_values)
        
        self.gen_graph(reduced_vectors, clustered_labels, description_vectors)
        # community_graph = b64encode(open('graph.png', 'rb').read())
        # community_graph = community_graph.decode('utf-8')

        communities = fake_community_detection(docs)
        
        return {
            # 'community_graph': community_graph,
            # 'connection_graph': connection_graph,
            'communities': communities
        }


    def gen_graph(self, reduced_vectors, clustered_labels, description_vectors):
        colors = dict()
        colors[0]= 'red'
        colors[1]= 'blue'
        colors[2]= 'green'

        fig = plt.figure(figsize=(15,15))

        ax = fig.add_subplot(111, projection='3d')


        for i, (vec, l, name) in enumerate(zip(reduced_vectors, clustered_labels, description_vectors)):
            x, y, z = vec
            ax.scatter(x, y, z, color=colors[l], s=100, label=name, cmap='RdPu')
            ax.text(x+0.1*x, y+0.1*y, z+0.1*z, name, fontsize=16)

        plt.savefig(os.path.join(IMG_PATH, 'communities.png'))
        plt.clf()


    def _gen_docs(self, connections):
        docs = dict()
        for c in connections:
            for friend in connections[c]['friends']:
                try:
                    name = friend['name']
                    _id = friend['details']['id']
                    docs[name] = {
                                    'description': friend['details']['description'],
                                    'details': friend['details']
                    }
                except KeyError as ke:
                    print('{} end connection for {}'.format(ke, c))
        return docs

if __name__ == "__main__":
    com_model = CommunityDetectionModel()
    results = com_model.graph_it('aviral0')
    # print('results')
    print(results)