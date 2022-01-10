from node2vec.edges import HadamardEmbedder
from convert import convert_dot_to_networkx
from edge import get_edge_embeddings
import pytest

test_file_path = './out/ls.dot'

def test_get_edge_embeddings():
    G = convert_dot_to_networkx(test_file_path)
    assert G is not None

    wv = get_edge_embeddings(G)
    assert type(wv) is HadamardEmbedder

def test_get_edge_embeddings_when_G_is_None():
    with pytest.raises(TypeError):
        get_edge_embeddings(None)
    