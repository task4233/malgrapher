# import pygraphviz  # it requires A.draw()
from networkx.classes.multidigraph import MultiDiGraph
from networkx.classes.multigraph import MultiGraph
from networkx.drawing.nx_agraph import to_agraph
from networkx.readwrite import json_graph
import networkx as nx
from typing import Union
import json
import os


def convert_dot_to_networkx(
        dot_file_path: str,
        saved_file_path: str = '') -> Union[MultiDiGraph, MultiGraph]:
    if not os.path.exists(dot_file_path):
        print(f'{dot_file_path} does not exist')
        assert(os.path.exists(dot_file_path))
    if os.path.getsize(dot_file_path) == 0:
        print(f'{dot_file_path} is empty')
        assert(os.path.getsize(dot_file_path) > 0)

    print(f'converting {dot_file_path}...')

    # https://networkx.org/documentation/stable/reference/generated/networkx.drawing.nx_pydot.read_dot.html?highlight=read_dot#networkx.drawing.nx_pydot.read_dot
    G = nx.drawing.nx_pydot.read_dot(dot_file_path)

    if saved_file_path != '':
        A = to_agraph(G)
        A.draw(saved_file_path, format='png', prog='dot')

    return G


def save_networkx_as_json(G: Union[MultiDiGraph, MultiGraph], saved_path: str):
    with open(saved_path, 'w') as f:
        json.dump(json_graph.node_link_data(G), f)


if __name__ == '__main__':
    G = None
    try:
        G = convert_dot_to_networkx('./out/ls.dot', './out/ls.png')
    except Exception as e:
        print('convert: ', e)

    assert G is not None
    save_networkx_as_json(G, './out/ls.json')
