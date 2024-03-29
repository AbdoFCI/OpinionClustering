from sklearn.cluster import AgglomerativeClustering
import numpy as np

class Agglomerative:

    def __init__(self,similarity_method):
        """

        :param similarity_method: example tree_similarity , jaccurd
        """
        self.similarity_method = similarity_method

    def _create_similarity_matrix(self, tags):
        """

        :param tags: list of list of str
        :return: np.matrix n*n, n = len(opinion)
        """
        matrix = []
        for outer in tags:
            row = []
            for inner in tags:
                row.append(self.similarity_method(outer, inner))
            matrix.append(row)
        return 1 - np.matrix(matrix)

    def cluster(self, tags, n_clusters=4, affinity='precomputed', linkage='complete'):
        """

        :param tags: list of list of str opinions data
        :param n_clusters: number of clusters 3-9 clusters default (4)
        :param affinity: string or callable, default: “precomputed”
        :param linkage: str {“ward”, “complete”, “average”, “single”}, optional (default=”complete”)
        :return: model: Labels of each point
        """
        dest_matrix = self._create_similarity_matrix(tags)
        model = AgglomerativeClustering(n_clusters=n_clusters, affinity=affinity, linkage=linkage).\
            fit_predict(dest_matrix)
        return list(model)
