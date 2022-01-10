from convert import convert_dot_to_networkx
from graph import get_graph_embeddings, Graph
from gensim.models.doc2vec import Doc2Vec
import pytest

test_file_path = './out/ls.dot'


def test_get_graph_embeddings():
    g1 = Graph('ls', convert_dot_to_networkx('./out/ls.dot'))
    assert g1.graph is not None
    g2 = Graph('cat', convert_dot_to_networkx('./out/cat.dot'))
    assert g2.graph is not None    
    graphs = [g1, g2]

    model = get_graph_embeddings(graphs)
    assert type(model) is Doc2Vec

def test_get_graph_embeddings_with_single_graph():
    G = convert_dot_to_networkx(test_file_path)
    assert G is not None

    with pytest.raises(AssertionError):
            get_graph_embeddings(G)
