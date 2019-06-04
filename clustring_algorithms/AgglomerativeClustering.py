from sklearn.cluster import AgglomerativeClustering
import semantic_tree.Parser as pars
import numpy as np
import pandas as pd


class AgglomerativeClustering:

    def __init__(self,similarity_method):
        """

        :param similarity_method: example tree_similarity , jaccurd
        """
        self.similarity_method = similarity_method

    def _create_similarity_matrix(self, opinions):
        """

        :param opinions:list of list of str
        :return: np.matrix n*n, n = len(opinion)
        """
        matrix = []
        for outer in opinions:
            row = []
            for inner in opinions:
                row.append(self.similarity_method(outer, inner))
            matrix.append(row)
        return matrix

    def cluster(self,tags,n_clusters=4,affinity='precomputed' ,linkage='complete'):
        """

        :param tags:list of list of str opinions data
        :param n_clusters:number of clusters 3-9 clusters default (4)
        :param affinity:string or callable, default: “euclidean”
        :param linkage:str {“ward”, “complete”, “average”, “single”}, optional (default=”complete”)
        :return: Labels of each point
        """
        dest_matrix = self._create_similarity_matrix(tags)
        model = AgglomerativeClustering(affinity=affinity, n_clusters=n_clusters, linkage=linkage).\
            fit_predict(dest_matrix)
        return list(model)
