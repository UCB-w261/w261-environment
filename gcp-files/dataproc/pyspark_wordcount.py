import pyspark

sc = pyspark.SparkContext()

input = 'gs://w261-data/words.txt'
output = 'gs://w261-data/word_count.txt'

rdd = sc.textFile(input)
counts = rdd.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b) \
             .repartition(1) \
             .saveAsTextFile(output)
