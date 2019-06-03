from Tag2vec import HashTag2Vec
from pyspark.ml.clustering import KMeans

class KMeansClustring:

    def __init__(self,spark_object):
        self.sparkContext = spark_object.getSparkContext()
        self.sqlContext = spark_object.getSQLContext()

    def cluster(self,tags, n_clusters=2,permutation=True,permutation_drop=0.5,method="sum"):
        tag2vec = HashTag2Vec(permutation=permutation,permutation_drop=permutation_drop, method=method)
        tag2vec.train(tags,window=6, alpha=0.03, epochs=10,vic_size=150,min_count=1)
        vectors = list(map(tag2vec.op2vec,tags))
        vec_rdd = self.sparkContext.parallelize(vectors)
        dataframe = vec_rdd.toDF(["hashtags"])
        kmeans = KMeans(featuresCol="hashtags", k=n_clusters)
        model=kmeans.fit(dataframe)
        return model