from tag2vec import hashtag2vec
from pyspark.mllib.clustering import KMeans


class KMeansClustering:

    def __init__(self, spark_object):
        """

        :param spark_object: SparkConnections object
        """
        self.sparkContext = spark_object.get_spark_context()
        self.sqlContext = spark_object.get_sql_context()

    def cluster(self, tags, n_clusters=2, permutation=True, permutation_drop=0.5, method="sum"):
        """

        :param tags: list of list of str opinions data
        :param n_clusters: number of clusters 3-9 clusters default (2)
        :param permutation: boolean tag2vec permutation in learning phase default (True)
        :param permutation_drop: float [0-1] drop of total permutation default (0.5)
        :param method: str method used to compute the feature vector of hash-tags default (sum)
        :return: clusters: Labels of each point
        """
        tag2vec = hashtag2vec.HashTag2Vec(permutation=permutation, permutation_drop=permutation_drop, method=method)
        tag2vec.train(tags, window=6, alpha=0.03, epochs=10, vic_size=150, min_count=1)
        vectors = list(map(tag2vec.op2vec, tags))
        vec_rdd = self.sparkContext.parallelize(vectors)
        model = KMeans.train(vec_rdd, k=n_clusters)
        clusters = model.predict(vec_rdd).collect()
        return clusters
