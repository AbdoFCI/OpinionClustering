from pyspark.mllib.clustering import PowerIterationClustering, PowerIterationClusteringModel


class PIC:

    def __init__(self, similarity_method, spark_object):
        """

        :param similarity_method: example tree_similarity , jaccard, edit distance
        """

        self.similarity_method = similarity_method
        self.sparkContext = spark_object.getSparkContext()
        self.sqlContext = spark_object.getSQLContext()

    def _create_similarities_list(self, opinions, threshold=0.05):
        """

        :param opinions: list of vector of string
        :param threshold: double
        :return: similarities list : list of tuples
        """
        similarities_list = []
        outer_id = 0
        inner_id = 0
        for outer in opinions:
            outer_id = outer_id + 1
            for inner in opinions:
                inner_id = inner_id + 1
                similarity = self.similarity_method(outer, inner)
                if similarity >= threshold:
                    similarities_list.append((outer_id, inner_id, similarity))
            inner_id = 0
        return similarities_list

    def cluster(self, tags, n_clusters=4, threshold=0.05, n_iterations=25, initialization_mode="degree"):
        """

        :param tags: list of vector of string
        :param n_clusters: number of cluster 
        :param threshold: double
        :param n_iterations: number of iterations
        :param initialization_mode: string ("degree", "random")
        :return: model
        """
        similarities_list = self._create_similarities_list(tags, threshold=threshold)
        rdd_data = self.sparkContext.parallelize(similarities_list)
        model = PowerIterationClustering.\
            train(rdd_data, n_clusters,n_iterations, initialization_mode)
        model_degr = model.assignments().collect()
        model_degr.sort()
        model = [assignment[1] for assignment in model_degr]
        return model
