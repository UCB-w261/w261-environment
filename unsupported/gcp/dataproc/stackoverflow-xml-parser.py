from pyspark.sql import SparkSession

spark = SparkSession\
        .builder\
        .getOrCreate()

df = spark.read\
    .format("com.databricks.spark.xml")\
    .options(rowTag="users")\
    .load("gs://w261-data/Stackoverflow/3dprinting.stackexchange.com/Users.xml")

df.printSchema()

print(df.head(2))
