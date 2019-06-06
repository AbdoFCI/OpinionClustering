from sklearn.cluster import AgglomerativeClustering
import numpy as np

class Agglomerative:

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
        return 1 - np.matrix(matrix)

    def cluster(self, tags, n_clusters=4, affinity='precomputed', linkage='complete'):
        dest_matrix = self._create_similarity_matrix(tags)
        model = AgglomerativeClustering(n_clusters=n_clusters, affinity=affinity, linkage=linkage).\
            fit_predict(dest_matrix)
        return list(model)
