from typing import Union
from gensim.models.keyedvectors import KeyedVectors

from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.multigraph import MultiGraph

from node2vec import Node2Vec
from convert import convert_dot_to_networkx


def get_node_embedings(
        G: Union[MultiDiGraph, MultiGraph],
        dims: int = 64,
        walk_length: int = 30,
        num_walks: int = 200,
        workers: int = 4,
        window_size: int = 10,
        min_count: int = 1,
        batch_words: int = 4,
        debug: bool = False) -> KeyedVectors:
    if G is None:
        raise TypeError('A type of G must be MultiDiGraph or MultiGraph')

    node2vec = Node2Vec(G, dimensions=dims, walk_length=walk_length,
                        num_walks=num_walks, workers=workers)
    model = node2vec.fit(window=window_size,
                         min_count=min_count, batch_words=batch_words)

    if debug:
        for node in G.nodes():
            print('similar vector: ', node)
            print('similar_node', model.wv.most_similar(node))
            print('')

    return model.wv


if __name__ == '__main__':
    try:
        G = convert_dot_to_networkx('./out/ls.dot')
        wv = get_node_embedings(G)
    except Exception as e:
        print('embeddings: ', e)
