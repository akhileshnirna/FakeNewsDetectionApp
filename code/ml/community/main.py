from collections import OrderedDict as dict
from twitter import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from api_helper import get_top_friends
from graph_helper import generate_graph_from_connections, viz_graph
from community import vectorize, spectral_cluster, pca
from community import fake_community_detection
from base64 import b64encode

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

class CommunityDetectionModel():
    
    def __init__(self):
        self.twitter = Twitter(auth=OAuth(
                access_token,
                access_token_secret,
                consumer_key,
                consumer_secret
                )
        )
    
    def graph_it(self, user_name, num_friends_at_depths=[2, 2, 2], n_clusters=3):
        self.user_name = user_name
        connections = get_top_friends(self.twitter, self.user_name, 
                            friends_at_depths=num_friends_at_depths)
        
        connection_graph = generate_graph_from_connections(connections)
        viz_graph(connection_graph, save_graph=True, file_name='demo.png')
        connection_graph = b64encode(open('demo.png', 'rb').read())

        docs = self._gen_docs(connections)
        
        description_vectors = vectorize(docs)
        vector_values = list(description_vectors.values())
        
        clustered_labels = spectral_cluster(vector_values, n_clusters=n_clusters)

        for user_name, cluster_label in zip(description_vectors.keys(), clustered_labels):
            docs[user_name]['community'] = cluster_label

        reduced_vectors = pca(vector_values)
        
        self.gen_graph(reduced_vectors, clustered_labels, description_vectors)
        community_graph = b64encode(open('graph.png', 'rb').read())

        communities = fake_community_detection(docs)
        
        return {
            'community_graph': community_graph,
            'connection_graph': connection_graph,
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

        plt.savefig('graph.png')


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