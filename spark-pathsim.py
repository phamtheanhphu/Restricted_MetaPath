import os

from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

#declare the graphframe libraries
os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--packages graphframes:graphframes:0.5.0-spark2.1-s_2.11 pyspark-shell"
)

# from graphframes import *
sc = SparkSession \
    .builder \
    .appName("GraphFrameTest") \
    .getOrCreate()

sqlContext = SQLContext(sc)

# Create a Vertex DataFrame with unique ID column "id"
v = sqlContext.createDataFrame([
    ("a", "Alice", 34),
    ("b", "Bob", 36),
    ("c", "Charlie", 30),
], ["id", "name", "age"])

# Create an Edge DataFrame with "src" and "dst" columns
e = sqlContext.createDataFrame([
    ("a", "b", "friend"),
    ("b", "c", "follow"),
    ("c", "b", "follow"),
], ["src", "dst", "relationship"])

from graphframes import *
g = GraphFrame(v, e)

results = g.shortestPaths(landmarks=["a", "c"])
results.show()

results.select("id", explode("distances"))
results.show()