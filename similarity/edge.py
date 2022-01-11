from typing import Union

from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.multigraph import MultiGraph
from convert import convert_dot_to_networkx
from node import get_node_embedings
from node2vec.edges import HadamardEmbedder
import traceback


def get_edge_embeddings(G: Union[MultiDiGraph, MultiGraph], debug: bool = False) -> HadamardEmbedder:
    if G is None:
        raise TypeError(' A type of G must be MultiDiGraph or MultiGraph')

    wv = None
    try:
        wv = HadamardEmbedder(keyed_vectors=get_node_embedings(G))
    except Exception as e:
        raise e

    if debug:
        for idxI in range(len(G.nodes())):
            for idxJ in range(idxI):
                print('similar vector: ', (idxI, idxJ))
                print('similar_edge', wv.most_similar((idxI, idxJ)))
                print('')

    return wv


if __name__ == '__main__':
    try:
        G = convert_dot_to_networkx('./out/ls.dot')
        embeds = get_edge_embeddings(G)

    except Exception as e:
        print(traceback.format_exc())
