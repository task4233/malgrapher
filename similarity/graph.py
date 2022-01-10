from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.multigraph import MultiGraph
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import networkx as nx
from typing import List, Union
from weisfeiler_lehman import WeisfeilerLehmanMachine
from convert import convert_dot_to_networkx
import traceback
import pandas as pd
import os

class Graph:
    def __init__(self, name: str, graph: Union[MultiDiGraph, MultiGraph]) -> None:
        self.name = name
        assert graph is not None
        self.graph = graph

def get_features_from_graph(graph: Union[MultiDiGraph, MultiGraph]):
    features = nx.degree(graph)
    return {k: v for k, v in features}


def explore_subgraphs(name: str, graph: Union[MultiDiGraph, MultiGraph], rounds: int = 2) -> TaggedDocument:
    features = get_features_from_graph(graph)
    machine = WeisfeilerLehmanMachine(graph, features, rounds)
    return TaggedDocument(words=machine.extracted_features, tags=["g_" + name])


def get_graph_embeddings(
        graphs: List[Graph],
        dimensions: int = 128,
        window_size: int = 5,
        min_count: int = 5) -> Doc2Vec:

    assert type(graphs) is list

    graph_collections = [explore_subgraphs(
        graph.name, graph.graph) for graph in graphs]
    model = Doc2Vec(graph_collections,
                    vector_size=dimensions,
                    window=window_size,
                    min_count=min_count)
    return model

def save_embeddings(output_path: str, model: Doc2Vec, graphs: List[TaggedDocument], dimensions: int):
    if not os.path.exists(output_path):
        with open(output_path, 'wb') as f: pass
        
    out = []
    for graph in graphs:
        out.append([graph.name] + list(model.dv["g_"+graph.name]))
    
    column_names = ["types"]+["x_"+str(dim) for dim in range(dimensions)]
    out = pd.DataFrame(out, columns=column_names)
    out.to_csv(output_path, index=None)

if __name__ == "__main__":
    dimensions = 128

    try:
        g1 = Graph('ls', convert_dot_to_networkx('./out/ls.dot'))
        g2 = Graph('cat', convert_dot_to_networkx('./out/cat.dot'))
        graphs = [g1, g2]
        model = get_graph_embeddings(graphs, dimensions=dimensions)
        save_embeddings('./out/ls.model', model, graphs, dimensions)
    except Exception as e:
        print(traceback.format_exc())
