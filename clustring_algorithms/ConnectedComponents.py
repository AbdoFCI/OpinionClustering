from pyspark import *
from graphframes import *
from pyspark import sql


class ConnectedComponents:

    conf = SparkConf().setAppName("PySparkApp").setMaster("local[*]")
    sc = SparkContext(conf=conf)
    sc.setCheckpointDir(r'D:\checkpoints')
    sqlContext = sql.SQLContext(sc)

    def __init__(self, similarity_method):
        """

        :param similarity_method: example tree_similarity , jaccard
        """

        self.similarity_method = similarity_method

    def _create_similarities_list(self, opinions, threshold=0.3):
        """

        :param opinions:list of list of str
        :return:
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

    def cluster(self, tags, n_clusters=2, init_threshold=0.3, increment=0.1):
        # """
        #     Computes the connected components of the graph.
        #
        #     :param numOfVertices: Number of opinions
        #     :param edges: List of vectors each consists of two opinions and similarity between them
        #     :param k: Number of expected clusters (default: 2)
        #     :param initTh: Initial similarity threshold value (default: 0.3)
        #     :param increment: Threshold increment value (default: 0.1)
        #
        #     :return: DataFrame with new vertices column "component"
        # """

        similarities_list = self._create_similarities_list(tags, threshold=init_threshold)
        vertices = []
        for i in range(1, len(tags)+1):
            vertices.append([i])
        vertices_df = self.sqlContext.createDataFrame(vertices, ['id'])

        rdd_edges = self.sc.parallelize(similarities_list)
        filtered_edges = rdd_edges.filter(lambda edge: edge[2] <= init_threshold)
        edges_df = self.sqlContext.createDataFrame(filtered_edges, ['src', 'dst', 'Similarity'])

        graph = GraphFrame(vertices_df, edges_df)
        result = graph.connectedComponents()
        num_components = result.select("component").distinct().count()

        th = init_threshold
        while num_components < n_clusters:
            th = th + increment
            filtered_edges = filtered_edges.filter(lambda edge: edge[2] <= th)
            graph = GraphFrame(vertices_df, edges_df)
            result = graph.connectedComponents()
            num_components = result.select("component").distinct().count()

        return result
