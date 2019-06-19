from pyspark import SparkContext, SparkConf
from pyspark import sql


class SparkObject:
    spark_context = None
    sql_context = None

    def __init__(self,appName,masterURL="local[*]"):
        conf = SparkConf().setAppName(appName).setMaster(masterURL)
        self.spark_context = SparkContext(conf=conf)
        self.sql_context = sql.SQLContext(self.spark_context)

    def get_spark_context(self):
        """

        :return: context of spark object
        """
        return self.spark_context

    def get_sql_context(self):
        """

        :return: sql context of sql object
        """
        return self.sql_context

    def set_checkpoint_dir(self, path =r'C:\checkpoints'):
        """

        :param path: str path
        :return: None
        """
        self.spark_context.setCheckpointDir(path)
