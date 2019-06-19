from graphframes import *


class ConnectedComponents:

    def __init__(self, similarity_method, spark_object):
        """

        :param spark_object: SparkConnections object
        :param similarity_method: example tree_similarity , jaccard
        """

        self.similarity_method = similarity_method
        self.sparkContext = spark_object.get_spark_context()
        self.sqlContext = spark_object.get_sql_context()
        spark_object.set_checkpoint_dir()

    def _create_similarities_list(self, tags, threshold=0.3):
        """

        :param tags:list of list of str
        :param threshold: float range [0-1] similarity threshold default (0.3)
        :return: similarities_list: list of tuples
        """
        similarities_list = []
        outer_id = 0
        inner_id = 0
        for outer in tags:
            outer_id = outer_id + 1
            for inner in tags:
                inner_id = inner_id + 1
                similarity = self.similarity_method(outer, inner)
                if similarity >= threshold:
                    similarities_list.append((outer_id, inner_id, similarity))
            inner_id = 0
        return similarities_list

    def cluster(self, tags, n_clusters=2, init_threshold=0.3, increment=0.1):
        """
        Computes the connected components of the graph.
        :param tags: list of list of str opinions data
        :param n_clusters: number of clusters 3-9 clusters default (2)
        :param init_threshold: float range [0-1] similarity init threshold default (0.3)
        :param increment: float iteration increasing if init_threshold
        :return: result: dataframe carries id and lable of each point
        """
        similarities_list = self._create_similarities_list(tags, threshold=init_threshold)
        vertices = []
        for i in range(1, len(tags)+1):
            vertices.append([i])
        vertices_df = self.sqlContext.createDataFrame(vertices, ['id'])

        rdd_edges = self.sparkContext.parallelize(similarities_list)
        filtered_edges = rdd_edges.filter(lambda edge: edge[2] > init_threshold)
        edges_df = self.sqlContext.createDataFrame(filtered_edges, ['src', 'dst', 'Similarity'])

        graph = GraphFrame(vertices_df, edges_df)
        result = graph.connectedComponents()
        num_components = result.select("component").distinct().count()

        th = init_threshold
        while num_components < n_clusters and th + increment <= 1:
            th = th + increment
            filtered_edges = filtered_edges.filter(lambda edge: edge[2] > th)
            graph = GraphFrame(vertices_df, edges_df)
            result = graph.connectedComponents()
            num_components = result.select("component").distinct().count()

        return result
