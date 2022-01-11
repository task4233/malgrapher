from typing import Type
from gensim.models.keyedvectors import KeyedVectors
import pytest
from node import get_node_embedings
from convert import convert_dot_to_networkx

test_file_path = './out/ls.dot'


def test_get_node_embeddings():
    G = convert_dot_to_networkx(test_file_path)
    assert G is not None

    wv = get_node_embedings(G)
    assert type(wv) is KeyedVectors


def test_get_node_embeddings_when_G_is_None():
    with pytest.raises(TypeError):
        get_node_embedings(None)
