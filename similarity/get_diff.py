from convert import convert_dot_to_networkx
from generate_dot_by_radare2 import generate_dot_by_radare2
from gensim.models.keyedvectors import KeyedVectors
import glob
import pandas as pd

from typing import List
from graph import Graph, get_graph_embeddings

import os


class DataSet:
    def __init__(self, bin_file_path: str, sample_name: str) -> None:
        assert(os.path.exists(bin_file_path))
        self.bin_file_path = bin_file_path
        self.dot_file_path = ''

        assert(len(sample_name) > 0)
        self.sample_name = sample_name

    def set_dot_file_path(self, dot_file_path: str):
        assert(len(dot_file_path) > 0)
        self.dot_file_path = dot_file_path


def get_datasets(dir: str = './sample') -> List[DataSet]:
    assert(os.path.exists(dir))

    res = []

    files = glob.glob(os.path.join(dir, '**'))
    for file in files:
        if not os.path.exists(file):
            continue
        base_name = os.path.basename(file)
        if len(base_name) <= 0:
            continue

        res.append(DataSet(file, base_name))
        print(f'{base_name} is added!')

    return res


if __name__ == "__main__":
    datasets = get_datasets(dir='/bin/')

    graphs = []
    for dataset in datasets:
        dataset.set_dot_file_path(generate_dot_by_radare2(
            dataset.bin_file_path, dataset.sample_name))
        if not os.path.exists(dataset.dot_file_path):
            print(
                f'{dataset.dot_file_path} is not created. Please check the reason manually...')
            continue
        graphs.append(Graph(dataset.sample_name,
                      convert_dot_to_networkx(dataset.dot_file_path)))

    model = get_graph_embeddings(graphs)

    results = pd.DataFrame({}, columns=['1st Similar file', '1st Similarity Score',
                           '2nd Similar file', '2nd Similarity Score', '3rd Similar file', '3rd Similarity Score'])

    for graph in graphs:
        print(f'get files which are similar to {graph.name}')
        sim_files = model.dv.most_similar(f'g_{graph.name}')
        print(sim_files)
        print('-----------------------------------------------')

        results.loc[graph.name] = [
            sim_files[0][0], sim_files[0][1],
            sim_files[1][0], sim_files[1][1],
            sim_files[2][0], sim_files[2][1],
        ]

    results.to_csv('results/out.csv')
