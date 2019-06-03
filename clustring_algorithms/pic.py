from pyspark.mllib.clustering import PowerIterationClustering, PowerIterationClusteringModel
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark import sql
from semantic_tree import Parser as pars
import pandas as pd
import numpy as np



class PIC:

    conf = SparkConf().setAppName("PySparkApp").setMaster("local[*]")
    sc = SparkContext(conf=conf)
    sqlContext = sql.SQLContext(sc)

    def __init__(self,similarity_method):
        """

        :param similarity_method: example tree_similarity , jaccard, edit distance
        """

        self.similarity_method = similarity_method

    def _create_similarities_list(self, opinions, threshold = 0.5):
        """

        :param opinions:list of vector of string
		:param threshold: double 
        :return: similarities list : list of tupels 
        """
        similarities_list = []
        outer_id = 0
        inner_id = 0
        similarity = 0
        for outer in opinions:
            outer_id = outer_id + 1
            for inner in opinions:
                inner_id = inner_id + 1
                similarity = self.similarity_method(outer , inner)
                if similarity >= threshold: similarities_list.append((outer_id, inner_id, similarity))
            inner_id = 0
        return similarities_list

    def cluster(self,tags,n_clusters=4,threshold = 0.5, n_iterations = 25, initialization_mode = "degree"):
        """

        :param tags: list of vector of string
        :param n_clusters: number of cluster 
        :param threshold: double
        :param n_iterations: number of iterations
        :param initialization_mode: string ("degree", "random")
        :return: model
        """
        similarities_list = self._create_similarities_list(tags, threshold = threshold)
        rdd_data = self.sc.parallelize(similarities_list)
        model = PowerIterationClustering.\
            train(similarities=rdd_data, n_clusters=n_clusters,
                  n_iterations=n_iterations, initialization_mode=initialization_mode)
        return model
