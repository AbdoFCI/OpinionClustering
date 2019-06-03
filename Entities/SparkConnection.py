from pyspark import SparkContext, SparkConf
from pyspark import sql


class SparkObject:
    spark_context = None
    sql_context = None

    def __init__(self,appName,masterURL="local[*]"):
        conf = SparkConf().setAppName(appName).setMaster(masterURL)
        self.spark_context = SparkContext(conf=conf)
        self.sql_context = sql.SQLContext(self.spark_context)

    def getSparkContext(self):
        return self.spark_context

    def getSQLContext(self):
        return self.sql_context

    def setCheckpointDir(self,path = r'C:\checkpoints'):
        self.spark_context.setCheckpointDir(path)
