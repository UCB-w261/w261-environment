#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Sample pyspark script to be uploaded to Cloud Storage and run on
Cloud Dataproc.

Note this file is not intended to be run directly, but run inside a PySpark
environment.

This file demonstrates how to read from a GCS bucket. See README.md for more
information.
"""

# [START pyspark]
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
# [END pyspark]
